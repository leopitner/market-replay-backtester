import pandas as pd
from pathlib import Path

REQUIRED = {"timestamp", "open", "high", "low", "close", "volume"}

def load_bars(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    if not df["timestamp"].is_monotonic_increasing:
        raise ValueError("Timestamps must be strictly monotonically increasing.")
    if df[list(REQUIRED - {"timestamp"})].isna().any().any():
        raise ValueError("Data contains NaN values.")
    
    return df.reset_index(drop=True)