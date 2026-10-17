from pathlib import Path
import json
import typer
import yaml

from app.data.loader import load_bars
from app.engine.backtest_engine import BacktestEngine
from app.strategy.examples.ma_cross import MACrossStrategy
from app.analytics.metrics import summarize

app = typer.Typer()

def _load_cfg(p: Path) -> dict:
    return yaml.safe_load(p.read_text()) or {}

@app.command()
def backtest(
    config: Path = typer.Option(..., "--config", "-c", exists=True),
    data: Path = typer.Option(..., "--data", "-d", exists=True),
    out: Path = typer.Option(Path("/app/results"), "--out", "-o"),
):
    """Run a backtest as fast as possible."""
    bars = load_bars(data)
    strat = MACrossStrategy(**_load_cfg(config))
    result = BacktestEngine().run(bars, strat)
    out.mkdir(parents=True, exist_ok=True)
    result.equity_curve.to_frame("equity").to_parquet(out / "equity.parquet")
    (out / "summary.json").write_text(json.dumps(summarize(result), indent=2))
    typer.echo(f"Done → {out}")

@app.command()
def replay(
    config: Path = typer.Option(..., "--config", "-c", exists=True),
    data: Path = typer.Option(..., "--data", "-d", exists=True),
    speed: float = typer.Option(1.0, "--speed", "-s"),
):
    """Replay bars at N× speed (add pacing in a later iteration)."""
    bars = load_bars(data)
    typer.echo(f"Replaying {len(bars)} bars at {speed}x (no-op stub for now)")
    for _ in bars.itertuples():
        pass

if __name__ == "__main__":
    app()