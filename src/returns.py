import numpy as np 
import pandas as pd

def calculate_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the daily log returns from price data.
    """
    if (prices <= 0).any().any():
        raise ValueError("Prices must be positive to calculate log returns")

    log_returns = np.log(prices / prices.shift(1))
    return log_returns.dropna()



def annualize_mean_returns(log_returns: pd.DataFrame, trading_days: int = 252) -> pd.Series:
    """
    Annualize average daily log returns.
    """

    return log_returns.mean() * trading_days


def annualize_covariance(log_returns: pd.DataFrame, trading_days: int = 252) -> pd.DataFrame:
    """
    Annualize covariance matrix of daily log returns.
    """
    return log_returns.cov() * trading_days

