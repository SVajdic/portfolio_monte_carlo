# Monte Carlo Portfolio Risk Simulator

## Overview

This project uses Monte Carlo simulation to model future portfolio performance and evaluate investment risk. Historical market data is used to estimate expected returns, volatility, and asset correlations, which are then used to generate thousands of possible future portfolio outcomes.

The simulator evaluates multiple portfolio allocation strategies and calculates common risk metrics such as Value at Risk (VaR), Conditional Value at Risk (CVaR), probability of loss, and maximum drawdown.

---

## Features

### Simulation and Risk Analysis
- Historical price data analysis
- Log return calculation
- Annualized return and covariance estimation
- Correlated asset simulations using Geometric Brownian Motion
- Multiple portfolio allocation strategies
- Monte Carlo simulation of future portfolio values
- Risk metric calculation:
    - Value at Risk (VaR)
    - Conditional Value at Risk (CVaR)
    - Probability of Loss
    - Maximum Drawdown
- Visualization of simulated portfolio paths
- Distribution analysis of final portfolio values
- CSV report generation

### Software and Performance
- Supports serial and parallel simulation modes
- Parallelization execution by computing batch-level risk summaries inside worker processes
- Uses command-line arguments to configure simulation count, trading horizon, work count, and random seed
- Benchmarks runtime across different simulation sizes
- Organizes code into modular data loading, simulation, risk metric, plotting, and parallel execution components

---

## Technologies
- Python
- NumPy
- Pandas
- Matplotlib
- yfinance

---

## Project Structure

```text
portfolio_monte_carlo/
├── README.md
├── data/
├── download_prices.py
├── main.py
├── outputs/
│   ├── figures/
│   └── reports/
├── requirements.txt
└── src/
    ├── __init__.py
    ├── data_loader.py
    ├── download_data.py
    ├── returns.py
    ├── risk_metrics.py
    ├── simulation.py
    ├── parallel.py
    └── visualization.py

```

---

## Methodology

### Historical Data

Historical adjusted closing prices are downloaded and stored locally.

Example assets:

- SPY (S&P 500 ETF)
- QQQ (Nasdaq-100 ETF)
- TLT (20+ Year Treasury Bond ETF)
- GLD (Gold ETF)

---

### Return Estimation

Daily log returns are calculated by:

```text
r_t = ln(P_t / P_(t-1))
```

where:

- `P_t` is the asset price at time `t`
- `P_(t-1)` is the asset price the previous time step

These returns are used to estimate:

- Expected annual return
- Annualized covariance matrix

---

### Monte Carlo Simulation

Future asset prices are simulated using Geometric Brownian Motion:

```text
S_(t+1) = S_t * exp(
    (μ - 0.5σ²)Δt + σ√Δt Z
)
```
where:

- `μ` = expected return
- `σ` = volatility
- `Δt` = time step
- `Z` = standard normal random variable

Asset correlations are incorporated using Cholesky decomposition of the covariance matrix

---

### Portfolio Evaluation

The simulator compares multiple allocation stragies:

- Equal Weight
- Aggressive Growth
- Defensive

Each portfolio is evaluated across thousands of simulated market scenarios

---

### Risk Metrics

#### Value at Risk (VaR)

Measures the loss threshold at a chosen confidence level.

Example:

95% VaR = 12%

Interpretation:
    There is a 5% porbability that the portfolio will lose more than 12% over the simulation horizon.


#### Conditional Value at Risk (CVaR)

Measures the average loss beyond the VaR threshold

#### Probablity of Loss

The fraction of simulations that finish below the initial portfolio value

#### Maximum Drawdown

The largest peak-to-trough decline experienced during a simulation

---

## Example Generated Outputs

```text
outputs/
├── figures/
│   ├── final_value_distribution_aggressive.png
│   ├── final_value_distribution_defensive.png
│   ├── final_value_distribution_equal_weight.png
│   ├── simulated_paths_aggressive.png
│   ├── simulated_paths_defensive.png
│   └── simulated_paths_equal_weight.png
└── reports/
    └── risk_summary.csv
```

|Portfolio|Mean Final Value |VaR 95|CVaR 95|Probability of Loss|Average Max Drawdown|5th Percentile|
|----|----|----|----|----|----|----|
|Equal Weight|10961.56|0.092|0.13|0.23|-0.096|9079.12|
|Aggressive|11303.32|0.12|0.17|0.24|-0.12|8737.97|
|Defensive|10978.95|0.099|0.13|0.23|-0.10|9006.677|

|Portfolio| Number of Simulations|Serial Run Time (s)|Parallel Run Time (s)|
|---|---|---|---|
|Equal Weight|10^4|0.317|0.345|
|Equal Weight|10^5|5.023|5.032|
|Equal Weight|10^6|55.162|57.292|
|Aggressive|10^4|0.318|0.298|
|Aggressive|10^5|4.426|4.472|
|Aggressive|10^6|55.328|53.983|
|Defensive|10^4|0.323|0.324|
|Defensive|10^5|4.211|4.277|
|Defensive|10^6|53.705|55.689|

### Notes
- No meaningful gains from using parallel mode 
- Pandas appears to be sufficently optimized compared to the added overhead of parallelization
- 10^7 simulations requires source code modifications in order not to overflow memory

---

## Installation

Clone the repository:

```bash
git clone https://github.com/SVajdic/portfolio_monte_carlo
cd portfolio_monte_carlo
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Download historical market data:

```bash
python download_prices.py
```

Run the simulation:
```bash
python main.py
```

Command line options:
```bash
options:
  -h, --help            show this help message and exit
  --mode {serial,parallel}
                        Run simulations serially or in parallel
  --n-simulations N_SIMULATIONS
                        Number of Monte Carlo simulations to run
  --n-workers N_WORKERS
                        Number of worker processes for parallel mode
  --trading-days TRADING_DAYS
                        Number of trading days to simulate
  --seed SEED           Random Seed number
  --initial-value INITIAL_VALUE
                        Initial portfolio value
```

Results will be written to:
`outputs/reports/`
`outputs/figures/`

---

## Future Improvements

- Efficient frontier optimization
- Sharpe ratio analysis
- Portfolio rebalancing
- Historical stress testing
- Bootstrap-based simulations
- Interactive dashoard using Dash or Streamlit

---

## Author

Stephan Vajdic

M.S. Physics | Python | C++ | Data Analysis| Statistical Modeling
