from pathlib import Path 
import pandas as pd 

def load_price_data(filepath: str | Path) -> pd.DataFrame:
    """
    Load historical asset prices from a CSV file.

    Expected format:
        Date,AAPL,MSFT,SPY
        2020-01-01,100.0,150.0,320.0

    Returns
    -------
    pd.DataFrame
        Date-indexed asset price dataframe
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Could not find file: {filepath}")
    
    prices = pd.read_csv(filepath, parse_dates=["Date"])
    prices = prices.set_index("Date")
    prices = prices.sort_index()

    if prices.empty:
        raise ValueError("Price dataframe is empty.")

    if prices.isnull().any().any():
        prices = prices.ffill().dropna()

    return prices