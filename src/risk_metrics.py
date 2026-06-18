import numpy as np


def final_values(portfolio_paths: np.ndarray) -> np.ndarray:
    return portfolio_paths[:,-1]


def portfolio_returns(portfolio_paths: np.ndarray) -> np.ndarray:
    initial_values = portfolio_paths[:,0]
    ending_values = portfolio_paths[:,-1]
    return ending_values / initial_values - 1



def value_at_risk(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    """
    VaR reported as a positive loss value

    Example:
        VaR = 0.12 means a 12% loss threshold at the selected confidence level.
    """
    percentile = 100 * (1 - confidence_level)
    return -np.percentile(returns, percentile)



def conditional_value_at_risk(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    """
    CVaR reported as a positive expected tail loss
    """
    var_threshold = np.percentile(returns, 100 * (1 - confidence_level))
    tail_losses = returns[returns <= var_threshold]

    if len(tail_losses) == 0:
        return 0.0
    
    return -tail_losses.mean()



def probability_of_loss(returns: np.ndarray) -> float:
    return np.mean(returns < 0)



def max_drawdown(path: np.ndarray) -> float:
    running_max = np.maximum.accumulate(path)
    drawdowns = path / running_max - 1
    return drawdowns.min()




def average_max_drawdown(portfolio_paths: np.ndarray) -> float:
    drawdowns = np.array([max_drawdown(path) for path in portfolio_paths])
    return drawdowns.mean()