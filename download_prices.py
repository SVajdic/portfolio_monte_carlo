from src.download_data import download_adjusted_close_prices


def main() -> None:
    tickers = ["SPY", "QQQ", "TLT", "GLD"]
    download_adjusted_close_prices(
        tickers=tickers,
        start_date="2015-01-01",
        end_date="2024-12-31",
        output_path="data/prices.csv"
    )


if __name__ == "__main__":
    main()