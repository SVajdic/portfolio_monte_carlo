from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np


def run_simulation_batch(
    batch_id: int,
    batch_size: int,
    initial_value: float,
    mean_returns,
    covariance_matrix,
    weights: np.ndarray,
    n_days: int,
    random_seed: int,
    simulation_function,
):
    """
    Run one independent Monte Carlo simulation batch

    This function is designed to be executed inside a worker process.
    """
    paths = simulation_function(
        initial_value=initial_value,
        mean_returns=mean_returns,
        covariance_matrix=covariance_matrix,
        weights=weights,
        n_days=n_days,
        n_simulations=batch_size,
        random_seed=random_seed + batch_id,
    )

    return paths

def run_parallel_simulations(
    initial_value: float,
    mean_returns,
    covariance_matrix,
    weights: np.ndarray,
    n_days: int,
    n_simulations: int,
    n_workers: int,
    random_seed: int,
    simulation_function,
):

    """
    Split simulations into independent batchs and run them in parallel
    """
    batch_size = n_simulations // n_workers
    remainder = n_simulations % n_workers

    batch_sizes = [
        batch_size + (1 if i < remainder else 0)
        for i in range(n_workers)
    ]

    results = []

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = []

        for batch_id, current_batch_size in enumerate(batch_sizes):
            future = executor.submit(
                run_simulation_batch,
                batch_id,
                current_batch_size,
                initial_value,
                mean_returns,
                covariance_matrix,
                weights,
                n_days,
                random_seed,
                simulation_function,
            )
            futures.append(future)

        for future in as_completed(futures):
            results.append(future.result())

    return np.vstack(results)