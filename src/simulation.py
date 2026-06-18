import numpy as np
import pandas as pd


def validate_weights(weights: np.ndarray, n_assets: int) -> None:
    if len(weights) != n_assets:
        raise ValueError(f"Expected {n_assets} weights, got {len(weights)}.")

    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("Portfolio weights must sum to 1.0")

    

def simulate_portfolio_paths(
    initial_value: float,
    mean_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    weights: np.ndarray,
    n_days: int = 252,
    n_simulations: int = 10000,
    random_seed: int | None = 42,
) -> np.ndarray:
    """
    Simulate portfolio value paths using correlated geometric Brownian motion.

    Returns
    -------
    np.ndarray
        Shape: (n_simulations, n_days + 1)
    """
    if initial_value <= 0:
        raise ValueError("Initial portfolio must be positive")

    n_assets = len(mean_returns)
    validate_weights(weights, n_assets)
    
    rng = np.random.default_rng(random_seed)

    dt = 1 / 252

    mean_vector = mean_returns.values
    cov_matrix = covariance_matrix.values

    cholesky_matrix = np.linalg.cholesky(cov_matrix)

    portfolio_paths = np.zeros((n_simulations, n_days + 1))
    portfolio_paths[:,0] = initial_value

    asset_prices = np.ones((n_simulations, n_assets))

    for day in range(1, n_days + 1):
        independent_randoms = rng.standard_normal((n_simulations, n_assets))
        correlated_randoms = independent_randoms @ cholesky_matrix.T 

        daily_returns = np.exp(
            (mean_vector - 0.5 * np.diag(cov_matrix)) * dt
            + correlated_randoms * np.sqrt(dt)
        )

        asset_prices *= daily_returns
        portfolio_paths[:, day] = initial_value * (asset_prices @ weights)

    return portfolio_paths