r"""
Faithful "robust arm" for the BERNER decomposition: C' and D'.

A reviewer flagged that the earlier arm C (closures objective, but the REAL
workload signal under a loose cap) is a hybrid: the cap was sized for the inflated
closure line counts while the workload imposed was the real one, so the constraint
went artificially slack and C behaved like the capacity-only arm D. The faithful
reproduction of the original method ("build the transformed instance and solve it as
its own self-consistent problem") feeds the closure-derived workload AND the loose
cap together, so the solver faces a genuine, near-binding balancing constraint:

    C' = closures objective, workload signal = bar_L (closure line counts), cap = loose T_s
    D' = nominal  objective, workload signal = bar_L,                        cap = loose T_s

bar_L_p (orders whose closure contains p) equals the popularity of p's pattern,
since the cover is a partition. C' is exactly "solve the enlarged instance"; D' is
its nominal control under the same closure-workload regime. The decomposition then is

    C' - D'  = the enlargement's own effect INSIDE the faithful closure regime
    D' - A   = the closure-workload-regime change, with no enlargement

CRUCIAL EXTRA CHECK. C'/D' optimise against a FICTIONAL workload (bar_L, counts of
closures that were never actually ordered). When the layout is deployed and the REAL
orders arrive, the real workload is L_p, not bar_L. So we recheck every C'/D' layout
against the REAL per-product pick-lines L_p and the REAL T_s. A gain earned by a
layout that violates the real workload constraint is not a deployable gain. (The real
feasibility is computed here directly, normalising station-id types, because the
Hexaly model only enforced the closure-world constraint it was given.)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import berner_decompose as bd  # reuse helpers


def real_feasibility(layout: Dict[str, str], stations: List[dict],
                     real_lines: Dict[str, int]) -> Tuple[int, int, float]:
    """Check a layout against the REAL workload L_p and REAL T_s (type-safe)."""
    speeds = {str(s["STATION_ID"]): float(s["SPEED"]) for s in stations}
    tcap = {str(s["STATION_ID"]): float(s["TIME_CAPACITY"]) for s in stations}
    caps = {str(s["STATION_ID"]): int(s["CAPACITY"]) for s in stations}
    cnt: Counter = Counter()
    wl: Dict[str, float] = defaultdict(float)
    for p, sid in layout.items():
        sid = str(sid)
        cnt[sid] += 1
        wl[sid] += real_lines.get(p, 0) / speeds.get(sid, 1.0)
    cap_br = sum(1 for sid in caps if cnt[sid] > caps[sid])
    wl_br = sum(1 for sid in tcap if wl[sid] > tcap[sid])
    max_ratio = max((wl[sid] / tcap[sid] for sid in tcap if tcap[sid] > 0), default=0.0)
    return cap_br, wl_br, max_ratio


def run(fold_dir: str, prefix: str, cover_dir: str, k_grid: List[int],
        top_supports: int, place_time: int, slack: float,
        prior_csv: str, out_csv: str) -> None:
    tr = pd.read_csv(os.path.join(fold_dir, f"{prefix}_train_orders.csv"), sep=";")
    te = pd.read_csv(os.path.join(fold_dir, f"{prefix}_test_orders.csv"), sep=";")
    pdf = pd.read_csv(os.path.join(fold_dir, f"{prefix}_train_products.csv"), sep=";")
    sdf = pd.read_csv(os.path.join(fold_dir, f"{prefix}_train_stations.csv"), sep=";")

    products = ("PROD_" + pdf["PRODUCT_ID"].astype(str)).tolist()
    universe = products
    prod_lines = {f"PROD_{i}": int(n) for i, n in zip(pdf["PRODUCT_ID"], pdf["REAL_LINES"])}
    real_stations = sdf.to_dict(orient="records")

    tr_sets = bd._supports(tr)
    tr_op = {o: list(s) for o, s in tr_sets.items()}
    te_op = te.groupby("ORDER")["PRODUCT"].apply(list).to_dict()
    tr_lines = prod_lines
    te_lines = te.groupby("PRODUCT").size().to_dict()
    base_supports = bd._top_supports(tr_sets, top_supports)
    opA = {f"D{i}": sorted(s) for i, s in enumerate(base_supports)}

    # Baseline A and the old arms from the prior run (same baseline -> comparable G).
    prior = pd.read_csv(prior_csv)
    A = prior[prior.arm == "A_baseline"].iloc[0]
    NA, VA = float(A["N"]), float(A["V"])
    print(f"[C'/D'] baseline A: N={NA:.0f} V={VA:.0f} | train={len(tr_op)} test={len(te_op)} "
          f"|P|={len(products)} supports={len(base_supports)} realT_s={real_stations[0]['TIME_CAPACITY']}",
          flush=True)

    rows: List[Dict[str, object]] = []
    for k in k_grid:
        cpath = os.path.join(cover_dir, f"cover_{prefix}_k{k}.json")
        if not os.path.exists(cpath):
            print(f"  [skip k={k}] no cover", flush=True)
            continue
        payload = json.load(open(cpath))
        patterns = [frozenset(p) for p in payload["patterns"]]
        c_bar = float(payload.get("c_bar", 0.0))
        p2p = bd._prod2pat(patterns)

        # bar_L_p = popularity of p's pattern = closure line count (partition fast path).
        pat_pop = [0] * len(patterns)
        for s in tr_sets.values():
            for j in {p2p[p] for p in s if p in p2p}:
                pat_pop[j] += 1
        bar_lines = {p: (pat_pop[p2p[p]] if p in p2p else prod_lines.get(p, 0)) for p in products}

        opC = {f"D{i}": bd._closure(s, p2p, patterns) for i, s in enumerate(base_supports)}
        recal_stations = bd._recalibrated_stations(tr_sets, patterns, p2p, real_stations,
                                                   universe, slack)
        rT = recal_stations[0]["TIME_CAPACITY"]; aT = real_stations[0]["TIME_CAPACITY"]

        # C' : closures + bar_L workload + loose cap  (solve the transformed instance).
        # D' : nominal  + bar_L workload + loose cap  (nominal control, same regime).
        layCp = bd._place(opC, recal_stations, products, bar_lines, place_time)
        layDp = bd._place(opA, recal_stations, products, bar_lines, place_time)

        for arm, lay, obj in (("Cprime_closures", layCp, "closures"),
                              ("Dprime_nominal", layDp, "nominal")):
            if lay is None:
                print(f"  [{arm} k={k}] INFEASIBLE in closure regime", flush=True)
                rows.append({"k": k, "arm": arm, "c_bar": c_bar, "N": None, "V": None,
                             "PoR_pct": None, "G_pct": None, "real_cap_broken": None,
                             "real_wl_broken": None, "real_wl_max_ratio": None})
                continue
            N = bd._eval(lay, tr_op, real_stations, tr_lines)[0]
            V = bd._eval(lay, te_op, real_stations, te_lines)[0]
            por = 100.0 * (N - NA) / NA
            g = 100.0 * (VA - V) / VA
            # REAL-world feasibility of this closure-regime layout.
            rcap, rwl, rratio = real_feasibility(lay, real_stations, prod_lines)
            print(f"  {arm} k={k}: N={N} V={V} PoR={por:+.2f}% G={g:+.2f}% | "
                  f"REAL feas: cap_br={rcap} wl_br={rwl}/{len(real_stations)} "
                  f"max_real_wl/realT_s={rratio:.2f}x (T_s {aT}->{rT})", flush=True)
            rows.append({"k": k, "arm": arm, "c_bar": c_bar, "N": N, "V": V,
                         "PoR_pct": round(por, 3), "G_pct": round(g, 3),
                         "real_cap_broken": rcap, "real_wl_broken": rwl,
                         "real_wl_max_ratio": round(rratio, 3)})

    out = pd.DataFrame(rows)
    out.to_csv(out_csv, index=False)
    print(f"\n[C'/D'] wrote {out_csv}")

    # Headline: faithful decomposition next to the old arms.
    oldG = {(int(r.k), r.arm): r.G_pct for _, r in prior.iterrows() if r.arm != "A_baseline"}
    print("\n=== FAITHFUL DECOMPOSITION (G vs baseline A); REAL-feasibility flagged ===")
    print(f'{"k":>3} {"c_bar":>5} | {"G(Cprime)":>10} {"G(Dprime)":>10} {"Cp-Dp":>7} | '
          f'{"oldG(B)":>8} {"oldG(C)":>8} {"oldG(D)":>8} | C\'/D\' real_wl_broken')
    for k in k_grid:
        sub = out[out.k == k]
        if sub.empty:
            continue
        cp = sub[sub.arm == "Cprime_closures"]; dp = sub[sub.arm == "Dprime_nominal"]
        if cp.empty or dp.empty or cp["G_pct"].iloc[0] is None:
            continue
        gcp = cp["G_pct"].iloc[0]; gdp = dp["G_pct"].iloc[0]
        wlcp = cp["real_wl_broken"].iloc[0]; wldp = dp["real_wl_broken"].iloc[0]
        gB = oldG.get((k, "B_preproc"), float("nan"))
        gC = oldG.get((k, "C_v2full"), float("nan"))
        gD = oldG.get((k, "D_caponly"), float("nan"))
        print(f'{k:>3} {float(sub.c_bar.iloc[0]):>5.2f} | {gcp:>+9.2f}% {gdp:>+9.2f}% '
              f'{gcp-gdp:>+6.2f}% | {gB:>+7.2f}% {gC:>+7.2f}% {gD:>+7.2f}% | {wlcp}/{wldp}')


def main() -> None:
    p = argparse.ArgumentParser(description="BERNER faithful robust arm (C'/D') + real feasibility.")
    p.add_argument("--fold-dir", default="berner_topn")
    p.add_argument("--prefix", default="bern")
    p.add_argument("--cover-dir", default="berner_covers")
    p.add_argument("--k", nargs="+", type=int, default=[2, 3, 4, 6, 10])
    p.add_argument("--top-supports", type=int, default=4000)
    p.add_argument("--place-time", type=int, default=120)
    p.add_argument("--slack", type=float, default=1.10)
    p.add_argument("--prior-csv", default="berner_decompose_result.csv")
    p.add_argument("--out-csv", default="berner_decompose_cprime_result.csv")
    args = p.parse_args()
    run(args.fold_dir, args.prefix, args.cover_dir, args.k, args.top_supports,
        args.place_time, args.slack, args.prior_csv, args.out_csv)


if __name__ == "__main__":
    main()
