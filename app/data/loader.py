import pandas as pd
from pathlib import Path

REQUIRED = {"timestamp", "open", "high", "low", "close", "volume"}

def load_bars(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp").reset_index(drop=True)