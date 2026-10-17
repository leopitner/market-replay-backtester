# Event-Driven Market Replay & Backtester

A lightweight, reproducible backtesting engine built in Python. 

This tool uses an event-driven architecture to process historical data bar-by-bar. It enforces **next-bar execution** (the strategy decides on bar `T`, but the broker fills at the open of bar `T+1`) to prevent look-ahead bias. 

## Quick Start

To install docker, use [Docker](https://docs.docker.com/get-docker/).

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
- **`ledger.csv`**: A complete execution ledger containing decision time, execution time, side, quantity, fill price, transaction costs, remaining cash, and resulting position.
- **`manifest.json`**: A reproducibility manifest capturing the exact git revision, strategy configuration, data checksum (SHA-256), and software versions used for the run.

## Using Your Own Data

To run a backtest on your own data:
1. Place your CSV file in the local `data/` folder.
2. Ensure your CSV has the following columns:
   `timestamp, open, high, low, close, volume`
3. Run the container, pointing to your file:
   ```bash
   docker compose run --rm backtester backtest --config /app/config/example.yaml --data /app/data/my_data.csv
   ```

## Running Tests Locally

The test suite validates the execution logic against hand-calculated fixtures (proving next-bar fills, slippage, and ledger math) without needing Docker.

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

- [ ] MySQL-backed experiment history.
- [ ] Interactive market replay mode (pacing data in real-time).
- [ ] Multi-asset portfolio support.