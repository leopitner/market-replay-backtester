# Event-Driven Market Replay & Backtester

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

A lightweight, reproducible, and fully containerized market backtester and replay tool. 

Built with Python and Docker, this tool uses an event-driven architecture to process historical data, ensuring your strategies are tested without look-ahead bias. 

## Quick Start

To install Docker, use [Docker](https://docs.docker.com/get-docker/).

1. **Clone the repository:**
   git clone https://github.com/leopitner/market-replay-backtester.git
   cd market-replay-backtester

2. **Run the sample backtest:**
   docker compose run --rm backtester

3. **View results:**
   Check the `results/` folder on your local machine. You will find `summary.json` (Sharpe ratio, trades, final equity) and `equity.parquet` (a timeline of your portfolio value).

## Using Your Own Data

To run a backtest on your own data:
1. Place your CSV file in the `data/` folder.
2. Ensure your CSV has the following columns (order doesn't matter):
   `timestamp, open, high, low, close, volume`
3. Run the container, pointing to your file:
   docker compose run --rm backtester backtest --config /app/config/example.yaml --data /app/data/my_data.csv

## Writing a Custom Strategy

Strategies inherit from a simple base class. Check out `app/strategy/examples/ma_cross.py` for an example. 

Here is the basic template:

class MyStrategy(Strategy):
    def __init__(self, param1=10, **kwargs):
        super().__init__(**kwargs)
        self.param1 = int(param1)

    def on_bar(self, bar) -> int:
        # bar is a pandas Series with open, high, low, close, volume
        # Return 1 (Buy), -1 (Sell), or 0 (Do nothing)
        if bar["close"] > 100:
            return 1
        return 0

To run your strategy, update `config/example.yaml` and `app/main.py` to point to your new class.

## Architecture & Design

This project uses a strict event-driven architecture to ensure realism. For a deep dive into how the Event Loop, Simulated Broker, and Data Feed interact, see [DESIGN.md](DESIGN.md).

## Running Tests Locally

If you want to develop locally without Docker:
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest

## License

Distributed under the MIT License. See `LICENSE` for more information.