from pathlib import Path
import yfinance as yf 


def download_adjusted_close_prices(
    tickers: list[str],
    start_date: str,
    end_date: str,
    output_path: str | Path,
) -> None:
    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    prices = data["Close"]
    prices = prices.dropna()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prices.to_csv(output_path)