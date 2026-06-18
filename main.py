import numpy as np
import pandas as pd

from pathlib import Path

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
    n_simulations
):
    paths = simulate_portfolio_paths(
        initial_value=initial_value,
        mean_returns=mean_returns,
        covariance_matrix=covariance_matrix,
        weights=weights,
        n_days=n_days,
        n_simulations=n_simulations,
        random_seed=42,
    )

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
    }

    safe_name = name.lower().replace(" ", "_")

    plot_simulated_paths(
        paths, 
        f"outputs/figures/simulated_paths_{safe_name}.png")
    plot_final_value_distributions(
        endings, 
        f"outputs/figures/final_value_distribution_{safe_name}.png")

    return results

    #/print(f"\n{name}")
    #print("-" * 40)
    #print(f"Mean Final Value: ${endings.mean():,.2f}")
    #print(f"95% VaR: {var_95:.2%}")
    #print(f"95% CVaR: {cvar_95:.2%}")
    #print(f"5th Percentile Final Value: ${np.percentile(endings, 5):,.2f}")
    #print(f"Probability of Loss: {prob_loss:.2%}")
    #print(f"Average Max Drawdown: {avg_drawdown:.2%}")

def main() -> None:
    
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

    initial_value = 10_000
    n_days = 252
    n_simulations = 10_000

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
