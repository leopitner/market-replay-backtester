# System Architecture & Design

This document outlines the architectural decisions behind the Market Replay & Backtester.

## 1. Core Philosophy

### Determinism & Reproducibility
Backtesting is only useful if it is reproducible. By containerizing the entire application (pinning Python versions and library dependencies in the `Dockerfile`), we guarantee that a backtest run today will yield the exact same results next year, on a completely different machine.

### Avoiding Look-Ahead Bias
Many vectorized backtesters (using `pandas` or `numpy` across the whole dataset at once) suffer from subtle look-ahead biases. This project uses a strict **event-driven** architecture. The engine processes data bar-by-bar, meaning the strategy only ever sees the data up to the current timestamp.

## 2. High-Level Architecture

The system is divided into decoupled components that communicate via the `BacktestEngine`.

[ Data Loader ] ──> [ Strategy ] ──> [ Simulated Broker ] ──> [ Analytics ]
       │                 │                     │                    │
   (CSV/Parquet)    (on_bar logic)       (Slippage, Fees)      (Sharpe, PnL)

## 3. Component Breakdown

### `app/data/loader.py`
Responsible for ingesting raw CSV data. It enforces a strict schema (`timestamp, open, high, low, close, volume`) and handles datetime parsing. It sorts the data chronologically to prevent out-of-order execution errors.

### `app/engine/backtest_engine.py`
The heart of the system. It orchestrates the loop:
1. Pulls a bar from the Data Loader.
2. Passes the bar to the Strategy.
3. Receives a signal (`-1, 0, 1`).
4. If a signal is generated, it asks the Broker to execute the trade.
5. Records the current portfolio equity.

*(Note: A true event-loop using `heapq` is planned for future iterations to support multi-asset asynchronous event handling).*

### `app/strategy/base.py` & `examples/`
Strategies are entirely decoupled from execution. They are stateful objects that receive one bar at a time via the `on_bar()` method. They do not know about cash, positions, or slippage—they only output a signal. 

### `app/broker/simulated_broker.py`
A naive backtester will fill orders at the exact closing price. This broker applies **slippage** (e.g., 5 basis points) to every fill. This prevents strategies from producing unrealistic returns based on perfect execution.

### `app/analytics/metrics.py`
Calculates performance statistics. Currently, it computes the Sharpe Ratio, final equity, and total trade count. Output is serialized to JSON and Parquet for downstream analysis in Jupyter Notebooks or BI tools.

## 4. Containerization Strategy

The `Dockerfile` is designed with best practices for security and build speed:
* **Multi-stage builds (optional/planned):** Separates dependency compilation from the runtime image to reduce attack surface and image size.
* **Non-root User:** The container runs as `appuser` (UID 1000) instead of `root`. This prevents permission issues with mounted volume directories on the host machine (especially on Linux and macOS) and improves container security.
* **Volume Mounts:** The container treats code as immutable. Only `data/`, `config/`, and `results/` are mounted from the host. This means users can change their strategy parameters or input 10GB datasets without ever needing to rebuild the Docker image.

## 5. Future Roadmap
- [ ] Implement a true priority-queue event loop (`heapq`) for multi-asset backtesting.
- [ ] Add a WebSocket server to enable real-time market replay to frontend dashboards.
- [ ] Support Parquet and SQLite as input data sources.