# Event-Driven Bar-by-Bar Backtester

A lightweight, reproducible Python backtesting tool. 

This engine uses an event-driven architecture to process historical data strictly bar-by-bar. It enforces **next-bar execution** (the strategy decides on bar `T`, but the broker fills at the open of bar `T+1`) to prevent look-ahead bias, and uses **target-position accounting** to calculate exactly what needs to be bought or sold to reach the desired state.

## Quick Start

To install Docker, use [Docker](https://docs.docker.com/get-docker/).

1. **Clone the repository:**
   ```bash
   git clone https://github.com/leopitner/market-replay-backtester.git
   cd market-replay-backtester
   ```

2. **Run the sample backtest:**
   ```bash
   docker compose run --rm backtester
   ```

## Outputs

Every run generates three files in the local `results/` folder:

- **`summary.json`**: Performance metrics (final equity, annualized Sharpe ratio, max drawdown, total trades).
- **`ledger.csv`**: A complete execution ledger containing decision time, execution time, side, quantity, reference price, adjusted fill price, slippage costs, commission fees, remaining cash, and resulting position.
- **`manifest.json`**: A reproducibility manifest capturing the exact git revision (injected at build time), strategy configuration, data checksum (SHA-256), and software versions used for the run.

## Using Your Own Data

To run a backtest on your own data:
1. Place your CSV file in the local `data/` folder.
2. Ensure your CSV has the following columns:
   `timestamp, open, high, low, close, volume`
   *(Note: The loader strictly rejects duplicate timestamps, non-finite numeric values, and invalid OHLC relationships).*
3. Run the container, pointing to your file:
   ```bash
   docker compose run --rm backtester backtest --config /app/config/example.yaml --data /app/data/my_data.csv
   ```

## Running Tests Locally

The test suite validates the core execution logic against hand-calculated fixtures. It specifically proves:
- Next-bar open execution.
- Non-zero slippage deduction (ensuring costs are only applied once).
- Accurate ledger attribution and cash accounting.

You can run the test suite locally without Docker:

```bash
# Set up local environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest
```

## Roadmap (Not Yet Implemented)

This tool is currently a backtester, not a live-market replay platform. The following features are planned:

- [ ] Interactive market replay mode (pacing data in real-time).
- [ ] MySQL-backed experiment history.
- [ ] Multi-asset portfolio support.