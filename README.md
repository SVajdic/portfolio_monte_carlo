# Monte Carlo Portfolio Risk Simulator

## Overview

This project uses Monte Carlo simulation to model future portfolio performance and evaluate investment risk. Historical market data is used to estimate expected returns, volatility, and asset correlations, which are then used to generate thousands of possible future portfolio outcomes.

The simulator evaluates multiple portfolio allocation strategies and calculates common risk metrics such as Value at Risk (VaR), Conditional Value at Risk (CVaR), probability of loss, and maximum drawdown.

---

## Features
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

Daily log retruns are calculated by:

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

|Portfolio|Mean Final Value|VaR 95|CVaR 95|Probability of Loss|Average Max Drawdown|5th Percentile|
|----|----|----|----|----|----|----|
|Equal Weight|10961.56930365797|0.0920871013270901|0.1329437067926568|0.2338|-0.09663901939214672|9079.128986729098|
|Aggressive|11303.326335137004|0.12620247481274158|0.1762766911898625|0.2434|-0.12935261472180495|8737.975251872584|
|Defensive|10978.953977921437|0.09933228697898706|0.13968494183280605|0.2374|-0.10106104790122042|9006.67713021013|

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
- Parallelized simulation engine
- Interactive dashoard using Dash or Streamlit

---

## Author

Stephan Vajdic

M.S. Physics | Python | C++ | Data Analysis| Statistical Modeling
