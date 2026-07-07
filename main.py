import numpy as np
import pandas as pd
import argparse

from pathlib import Path
from time import perf_counter

from src.data_loader import load_price_data
from src.returns import (
    calculate_log_returns,
    annualize_covariance,
    annualize_mean_returns,
)
from src.simulation import simulate_portfolio_paths
from src.risk_metrics import (
    final_values,
    portfolio_returns,
    value_at_risk,
    conditional_value_at_risk,
    probability_of_loss,
    average_max_drawdown,
)
from src.visualization import (
    plot_simulated_paths,
    plot_final_value_distributions,
)
from src.parallel import run_parallel_simulations

def parse_args():
    parser = argparse.ArgumentParser(
        description="Monte Carlo portfolio risk simulator"
    )

    parser.add_argument(
        "--mode",
        choices=["serial","parallel"],
        default="serial",
        help="Run simulations serially or in parallel"
    )

    parser.add_argument(
        "--n-simulations",
        type=int,
        default=10_000,
        help="Number of Monte Carlo simulations to run",
    )

    parser.add_argument(
        "--n-workers",
        type=int,
        default=4,
        help="Number of worker processes for parallel mode",
    )

    parser.add_argument(
        "--trading-days",
        type=int,
        default=252,
        help="Number of trading days to simulate",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random Seed number",
    )

    parser.add_argument(
        "--initial-value",
        type=float,
        default=10_000,
        help="Initial portfolio value",
    )

    return parser.parse_args()

def build_portfolios(n_assets):
    return {
        "Equal Weight": np.repeat(1 / n_assets, n_assets),

        "Aggressive": np.array([
            0.10,
            0.60,
            0.10,
            0.20
        ]),

        "Defensive": np.array([
            0.20,
            0.10,
            0.50,
            0.20
        ])
    }

def evaluate_portfolio(
    name,
    weights,
    mean_returns,
    covariance_matrix,
    initial_value,
    n_days,
    n_simulations,
    use_parallel: bool = False,
    n_workers=4,
    random_seed=42
):

    start_time = perf_counter()

    if use_parallel:
        paths = run_parallel_simulations(
            initial_value=initial_value,
            mean_returns=mean_returns,
            covariance_matrix=covariance_matrix,
            weights=weights,
            n_days=n_days,
            n_simulations=n_simulations,
            n_workers=n_workers,
            random_seed=random_seed,
            simulation_function=simulate_portfolio_paths,
        )
    else:
        paths = simulate_portfolio_paths(
            initial_value=initial_value,
            mean_returns=mean_returns,
            covariance_matrix=covariance_matrix,
            weights=weights,
            n_days=n_days,
            n_simulations=n_simulations,
            random_seed=random_seed,
        )

    elapsed_time = perf_counter() - start_time

    print(f"Simulation Runtime: {elapsed_time:.3f} seconds")

    endings = final_values(paths)
    returns = portfolio_returns(paths)

    var_95 = value_at_risk(returns, confidence_level=0.95)
    cvar_95 = conditional_value_at_risk(returns, confidence_level=0.95)
    prob_loss = probability_of_loss(returns)
    avg_drawdown = average_max_drawdown(paths)

    results = {
        "Portfolio": name,
        "Mean Final Value": endings.mean(),
        "VaR 95": var_95,
        "CVaR 95": cvar_95,
        "Probability of Loss": prob_loss,
        "Average Max Drawdown": avg_drawdown,
        "5th Percentile": np.percentile(endings, 5),
        "Runtime Seconds": elapsed_time,
    }

#    safe_name = name.lower().replace(" ", "_")
#
#    plot_simulated_paths(
#        paths, 
#       f"outputs/figures/simulated_paths_{safe_name}.png")
#    plot_final_value_distributions(
#        endings, 
#        f"outputs/figures/final_value_distribution_{safe_name}.png")

    return results

def main() -> None:
    
    args = parse_args()
    n_simulations = args.n_simulations
    n_days = args.trading_days
    use_parallel = args.mode == "parallel"
    n_workers = args.n_workers
    random_seed = args.seed
    initial_value = args.initial_value

    print(f"Mode: {args.mode}")
    print(f"Simulations: {n_simulations}")
    print(f"Trading Days: {n_days}")
    print(f"Workers: {n_workers if use_parallel else 'N/A'}")
    print(f"Random Seed: {random_seed}")
    print(f"Inital Value: {initial_value}")

    #make sure we have a directory to put outputs
    Path("outputs/reports").mkdir(
        parents=True,
        exist_ok=True,
    )

    Path("outputs/figures").mkdir(
        parents=True,
        exist_ok=True,
    )

    prices = load_price_data("data/prices.csv")

    log_returns = calculate_log_returns(prices)
    mean_returns = annualize_mean_returns(log_returns)
    covariance_matrix = annualize_covariance(log_returns)

    n_assets = prices.shape[1]

    portfolios = build_portfolios(n_assets)

    print("Monte Carlo Portfolio Risk Report")
    print("---------------------------------")
    print(f"Assets: {list(prices.columns)}")   
    print(f"Initial Portfolio Value: ${initial_value:,.2f}")

    results = []

    for name, weights in portfolios.items():
        result = evaluate_portfolio(
            name,
            weights,
            mean_returns,
            covariance_matrix,
            initial_value,
            n_days,
            n_simulations,
        )
        results.append(result)

    report_df = pd.DataFrame(results)

    report_df.to_csv(
        "outputs/reports/risk_summary.csv",
        index=False
    )

if __name__ == "__main__":
    main()
