r"""
Fair, deployability-aware clean comparison for the BERNER covering robustness.

Settles two fairness concerns in one table, every arm at a per-station 120% margin,
single early/late temporal split, k in {2,3,4,6,10,15,20}:

  Regime 1 -- REAL (deployable gold standard):
    A = raw obj, real L_p, real T_s (120%)        baseline
    B = closure obj, real L_p, real T_s (120%)    robustness, deployable. Headline G(B).
  Regime 2 -- FAIR INFLATED (per-station 120%):
    T_s^fair = ceil(1.20 * sum_{p: a0(p)=s} bar_L_p / V_s)   (A's exact calibration on
    the inflated lines, using the saved pinning a0 = PINNED_STATION).
    C'' = closure obj, bar_L workload, T_s^fair   robustness, fair inflated regime
    D'' = raw obj,     bar_L workload, T_s^fair   control. Headline G(C'')-G(D'').
  Reference -- SLACK (non-deployable), kept per request:
    oldD = raw obj, real L_p, eq.10 flat-average loose cap  ("what loose capacity buys")

Every arm is rechecked for REAL feasibility (real L_p, real T_s): cap/wl broken and
worst overload ratio = the deflation/deployability diagnostic. A within-pair contrast
(B-A, C''-D'') holds the feasible set fixed, so the workload cancels and the
difference is the pure enlargement (robustness) effect; the scaling cannot fake it.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from collections import defaultdict
from typing import Dict, List

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import berner_decompose as bd
import berner_decompose_cprime as cp


def per_station_fair_stations(real_stations: List[dict], pinning: Dict[str, int],
                              bar_lines: Dict[str, int], margin: float = 1.20) -> List[dict]:
    """T_s^fair = ceil(margin * sum_{p pinned to s} bar_L_p / V_s): A's calibration, inflated."""
    speeds = {s["STATION_ID"]: float(s["SPEED"]) for s in real_stations}
    load: Dict[int, float] = defaultdict(float)
    for p, sid in pinning.items():
        load[sid] += bar_lines.get(p, 0) / speeds.get(sid, 1.0)
    out = []
    for s in real_stations:
        new = dict(s)
        new["TIME_CAPACITY"] = int(math.ceil(margin * load.get(s["STATION_ID"], 0.0)))
        out.append(new)
    return out


def run(fold_dir: str, prefix: str, cover_dir: str, k_grid: List[int],
        top_supports: int, place_time: int, margin: float, loose_slack: float,
        out_csv: str) -> None:
    tr = pd.read_csv(os.path.join(fold_dir, f"{prefix}_train_orders.csv"), sep=";")
    te = pd.read_csv(os.path.join(fold_dir, f"{prefix}_test_orders.csv"), sep=";")
    pdf = pd.read_csv(os.path.join(fold_dir, f"{prefix}_train_products.csv"), sep=";")
    sdf = pd.read_csv(os.path.join(fold_dir, f"{prefix}_train_stations.csv"), sep=";")

    products = ("PROD_" + pdf["PRODUCT_ID"].astype(str)).tolist()
    universe = products
    prod_lines = {f"PROD_{i}": int(n) for i, n in zip(pdf["PRODUCT_ID"], pdf["REAL_LINES"])}
    pinning = {f"PROD_{i}": int(s) for i, s in zip(pdf["PRODUCT_ID"], pdf["PINNED_STATION"])}
    real_stations = sdf.to_dict(orient="records")

    tr_sets = bd._supports(tr)
    tr_op = {o: list(s) for o, s in tr_sets.items()}
    te_op = te.groupby("ORDER")["PRODUCT"].apply(list).to_dict()
    tr_lines = prod_lines
    te_lines = te.groupby("PRODUCT").size().to_dict()
    base_supports = bd._top_supports(tr_sets, top_supports)
    opA = {f"D{i}": sorted(s) for i, s in enumerate(base_supports)}

    rows: List[Dict[str, object]] = []

    def score(kval, arm, regime, lay, c_bar, NA, VA):
        if lay is None:
            print(f"  [{arm} INFEASIBLE]", flush=True)
            rows.append({"k": kval, "arm": arm, "regime": regime, "c_bar": c_bar,
                         "N": None, "V": None, "PoR_pct": None, "G_pct": None,
                         "real_cap_broken": None, "real_wl_broken": None, "real_wl_max_ratio": None})
            return
        N = bd._eval(lay, tr_op, real_stations, tr_lines)[0]
        V = bd._eval(lay, te_op, real_stations, te_lines)[0]
        por = 100.0 * (N - NA) / NA if NA else 0.0
        g = 100.0 * (VA - V) / VA if VA else 0.0
        rcap, rwl, rratio = cp.real_feasibility(lay, real_stations, prod_lines)
        print(f"  {arm:14s} [{regime}] N={N} V={V} PoR={por:+.2f}% G={g:+.2f}% | "
              f"REAL cap_br={rcap} wl_br={rwl}/{len(real_stations)} max={rratio:.2f}x", flush=True)
        rows.append({"k": kval, "arm": arm, "regime": regime, "c_bar": c_bar,
                     "N": N, "V": V, "PoR_pct": round(por, 3), "G_pct": round(g, 3),
                     "real_cap_broken": rcap, "real_wl_broken": rwl,
                     "real_wl_max_ratio": round(rratio, 3)})

    # --- A baseline: raw, real workload, real cap (k=1). --------------------
    print(f"[clean] train={len(tr_op)} test={len(te_op)} |P|={len(products)} "
          f"supports={len(base_supports)} | placing A baseline...", flush=True)
    layA = bd._place(opA, real_stations, products, prod_lines, place_time)
    assert layA is not None, "A baseline infeasible"
    NA = bd._eval(layA, tr_op, real_stations, tr_lines)[0]
    VA = bd._eval(layA, te_op, real_stations, te_lines)[0]
    score(1, "A_baseline", "real", layA, 1.0, NA, VA)

    for k in k_grid:
        cpath = os.path.join(cover_dir, f"cover_{prefix}_k{k}.json")
        if not os.path.exists(cpath):
            print(f"  [skip k={k}] no cover", flush=True)
            continue
        payload = json.load(open(cpath))
        patterns = [frozenset(p) for p in payload["patterns"]]
        c_bar = float(payload.get("c_bar", 0.0))
        p2p = bd._prod2pat(patterns)
        pat_pop = [0] * len(patterns)
        for s in tr_sets.values():
            for j in {p2p[p] for p in s if p in p2p}:
                pat_pop[j] += 1
        bar_lines = {p: (pat_pop[p2p[p]] if p in p2p else prod_lines.get(p, 0)) for p in products}
        opC = {f"D{i}": bd._closure(s, p2p, patterns) for i, s in enumerate(base_supports)}
        fair_stations = per_station_fair_stations(real_stations, pinning, bar_lines, margin)
        loose_stations = bd._recalibrated_stations(tr_sets, patterns, p2p, real_stations,
                                                   universe, loose_slack)
        print(f"--- k={k} c_bar={c_bar:.2f} | fair T_s[s1..3]="
              f"{[fair_stations[i]['TIME_CAPACITY'] for i in range(3)]} "
              f"real={[real_stations[i]['TIME_CAPACITY'] for i in range(3)]}", flush=True)

        # B: closures, real workload, real cap (deployable robustness).
        score(k, "B_closures", "real", bd._place(opC, real_stations, products, prod_lines, place_time),
              c_bar, NA, VA)
        # C'': closures, bar_L workload, fair per-station cap.
        score(k, "Cpp_closures", "fair", bd._place(opC, fair_stations, products, bar_lines, place_time),
              c_bar, NA, VA)
        # D'': raw, bar_L workload, fair per-station cap (control for C'').
        score(k, "Dpp_nominal", "fair", bd._place(opA, fair_stations, products, bar_lines, place_time),
              c_bar, NA, VA)
        # oldD: raw, real workload, eq.10 loose cap (slack reference, non-deployable).
        score(k, "oldD_slack", "loose", bd._place(opA, loose_stations, products, prod_lines, place_time),
              c_bar, NA, VA)

    out = pd.DataFrame(rows)
    out.to_csv(out_csv, index=False)
    print(f"\n[clean] wrote {out_csv}")

    # Headline table.
    print("\n=== CLEAN COMPARISON (G vs A; * = real-infeasible/non-deployable) ===")
    print(f'{"k":>3} {"c_bar":>5} | {"G(B) real":>10} | {"G(Cpp) fair":>12} {"G(Dpp) fair":>12} '
          f'{"Cpp-Dpp":>8} | {"G(oldD)":>8} | deployable B/Cpp/Dpp')

    def gv(k, arm):
        r = out[(out.k == k) & (out.arm == arm)]
        return (r["G_pct"].iloc[0], r["real_wl_broken"].iloc[0]) if len(r) and r["G_pct"].iloc[0] is not None else (None, None)
    for k in k_grid:
        sub = out[out.k == k]
        if sub.empty:
            continue
        gB, wB = gv(k, "B_closures")
        gC, wC = gv(k, "Cpp_closures")
        gD, wD = gv(k, "Dpp_nominal")
        gO, _ = gv(k, "oldD_slack")
        if gB is None:
            continue
        cm = lambda w: "ok" if w == 0 else f"NO({w})"
        cd = (gC - gD) if (gC is not None and gD is not None) else float("nan")
        print(f'{k:>3} {float(sub.c_bar.iloc[0]):>5.2f} | {gB:>+9.2f}% | '
              f'{(gC if gC is not None else float("nan")):>+10.2f}% {(gD if gD is not None else float("nan")):>+10.2f}% '
              f'{cd:>+6.2f}% | {(gO if gO is not None else float("nan")):>+7.2f}% | {cm(wB)}/{cm(wC)}/{cm(wD)}')


def main() -> None:
    p = argparse.ArgumentParser(description="BERNER fair clean comparison (per-station 120% caps).")
    p.add_argument("--fold-dir", default="berner_topn")
    p.add_argument("--prefix", default="bern")
    p.add_argument("--cover-dir", default="berner_covers")
    p.add_argument("--k", nargs="+", type=int, default=[2, 3, 4, 6, 10, 15, 20])
    p.add_argument("--top-supports", type=int, default=4000)
    p.add_argument("--place-time", type=int, default=120)
    p.add_argument("--margin", type=float, default=1.20)
    p.add_argument("--loose-slack", type=float, default=1.10)
    p.add_argument("--out-csv", default="berner_clean_comparison_result.csv")
    args = p.parse_args()
    run(args.fold_dir, args.prefix, args.cover_dir, args.k, args.top_supports,
        args.place_time, args.margin, args.loose_slack, args.out_csv)


if __name__ == "__main__":
    main()
