from pathlib import Path
import json
import typer
import yaml
import pandas as pd
import hashlib
import subprocess
import sys

from app.data.loader import load_bars
from app.engine.backtest_engine import BacktestEngine
from app.strategy.examples.ma_cross import MACrossStrategy
from app.analytics.metrics import summarize

app = typer.Typer()

def _load_cfg(p: Path) -> dict:
    return yaml.safe_load(p.read_text()) or {}

def _get_git_rev() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
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
    
    strat = MACrossStrategy(**cfg)
    result = BacktestEngine().run(bars, strat)
    
    out.mkdir(parents=True, exist_ok=True)
    result.equity_curve.to_frame("equity").to_parquet(out / "equity.parquet")
    if not result.ledger.empty:
        result.ledger.to_csv(out / "ledger.csv", index=False)
        
    (out / "summary.json").write_text(json.dumps(summarize(result), indent=2))
    
    manifest = {
        "git_revision": _get_git_rev(),
        "config": cfg,
        "data_sha256": _hash_file(data),
        "versions": {
            "python": sys.version.split()[0],
            "pandas": pd.__version__
        }
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    
    typer.echo(f"Done → {out}")