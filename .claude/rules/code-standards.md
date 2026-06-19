# code-standards

This document establishes the Python coding conventions and solver implementation standards for the CSLAP optimization project. All agents writing or reviewing code must enforce compliance with these standards.

## 1. Directory & File Placement
* All solver implementations must reside inside the directory:
  `Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/`
* Filename naming pattern: Use snake_case with clear descriptive suffixes:
  * Stochastic models: `*_stochastic.py` (e.g., `milp_gurobi_stochastic.py` or `cg_gurobi_stochastic.py`)
  * Robust models: `*_robust.py`
  * Heuristics/Data adapters: `*_heuristic.py`

## 2. Command Line Interface (CLI)
Every python solver must expose a standard CLI interface using `argparse` with at least the following arguments:
* `--prefix`: Dataset prefix matching files in the dataset directory (e.g., `syn_50sku_corr0.5_1`).
* `--dir`: Directory path containing the dataset csv files (defaults to `synthetic_datasets`).
* `--time`: Timeout limit in seconds for the optimization solver (defaults to `120`).

Example Main block:
```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Description of the model")
    parser.add_argument("--prefix", type=str, required=True)
    parser.add_argument("--dir", type=str, default="synthetic_datasets")
    parser.add_argument("--time", type=int, default=120)
    # Add model-specific options here...
    args = parser.parse_args()
```

## 3. Data Loading Integration
Solvers must read input CSV files separated by semicolons (`;`) matching the standard CSLAP schema:
* `*_orders.csv`
* `*_stations.csv`
* `*_products.csv`

The data loading function should follow the pattern from `milp_gurobi_synthetic.py`:
```python
def read_data(prefix: str, data_dir: str):
    orders_df = pd.read_csv(os.path.join(data_dir, f"{prefix}_orders.csv"), sep=";")
    stations_df = pd.read_csv(os.path.join(data_dir, f"{prefix}_stations.csv"), sep=";")
    products_df = pd.read_csv(os.path.join(data_dir, f"{prefix}_products.csv"), sep=";")
    ...
    return order_prods, stations, products, prod_lines
```

## 4. Coding Style & Linting
* **Type Hints**: All functions must have explicit type hints for arguments and return types.
* **Docstrings**: All modules, classes, and public functions must have triple-quoted docstrings. Optimization models must list their mathematical formulations, variables, and constraints in LaTeX format within the docstring.
* **Gurobi Naming Conventions**:
  * Gurobi models should be named `model` or `m`.
  * Variables should use `model.addVar()` or `model.addVars()`.
  * Constraints should use `model.addConstr()` or `model.addConstrs()`.
  * Objective functions should use `model.setObjective()`.
* **Standard Return Interface**:
  The core runner/solver function must return the following tuple structure:
  `(assignment, total_visits, elapsed_time, util_variance, max_util, cap_broken, wl_broken, best_bound)`

## 5. Logging & Outputs
* **Console Logs**: Log key milestones, solve start, solver configuration params, objective values, final run stats, and solver termination status.
* **Standard Solver Outputs**: Ensure output CSV structures align with `results_syn_*.csv` formats.
