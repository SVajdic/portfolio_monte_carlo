from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt 



def plot_simulated_paths(
    portfolio_paths: np.ndarray,
    output_path: str | Path = "simulated_paths.png",
    max_paths: int = 200,
) -> None:
    output_path = Path(output_path)

    n_paths = min(max_paths, portfolio_paths.shape[0])

    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_paths[:n_paths].T, alpha=0.2)
    plt.xlabel("Trading Days")
    plt.ylabel("Portfolio Value")
    plt.title("Monte Carlo Simulated Portfolio Paths")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()



def plot_final_value_distributions(
    final_values: np.ndarray,
    output_path: str | Path = "final_value_distribution.png",
) -> None:
    output_path = Path(output_path)


    plt.figure(figsize=(10, 6))
    plt.hist(final_values, bins=60)
    plt.xlabel("Final Portfolio Value")
    plt.ylabel("Frequency")
    plt.title("Distribution of Final Portfolio Values")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()