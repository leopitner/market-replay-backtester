from pathlib import Path
import json
import typer
import yaml
import pandas as pd
import hashlib
import subprocess
import sys
import os

from app.data.loader import load_bars
from app.engine.backtest_engine import BacktestEngine
from app.strategy.examples.ma_cross import MACrossStrategy
from app.analytics.metrics import summarize

app = typer.Typer()

@app.callback()
def cli():
    """Market backtesting tools."""
    pass

def _load_cfg(p: Path) -> dict:
    return yaml.safe_load(p.read_text()) or {}

def _get_git_rev() -> str:
    env_rev = os.environ.get("GIT_REVISION")
    if env_rev:
        return env_rev
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
    except Exception:
        return "unknown"

def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

@app.command()
def backtest(
    config: Path = typer.Option(..., "--config", "-c", exists=True),
    data: Path = typer.Option(..., "--data", "-d", exists=True),
    out: Path = typer.Option(Path("/app/results"), "--out", "-o"),
):
    """Run a backtest."""
    bars = load_bars(data)
    cfg = _load_cfg(config)
    
    periods_per_year = cfg.pop("periods_per_year", 252)
    
    strat = MACrossStrategy(**cfg)
    result = BacktestEngine().run(bars, strat)
    
    out.mkdir(parents=True, exist_ok=True)
    result.equity_curve.to_frame("equity").to_parquet(out / "equity.parquet")
    
    ledger_cols = ["decision_time", "execution_time", "side", "quantity", "reference_price", "fill_price", "slippage_cost", "fees", "cash", "position"]
    if result.ledger.empty:
        pd.DataFrame(columns=ledger_cols).to_csv(out / "ledger.csv", index=False)
    else:
        result.ledger.to_csv(out / "ledger.csv", index=False)
        
    summary = summarize(result, periods_per_year=periods_per_year)
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    
    manifest = {
        "git_revision": _get_git_rev(),
        "config": cfg,
        "periods_per_year": periods_per_year,
        "data_sha256": _hash_file(data),
        "versions": {
            "python": sys.version.split()[0],
            "pandas": pd.__version__
        }
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    
    typer.echo(f"Done → {out}")

if __name__ == "__main__":
    app()