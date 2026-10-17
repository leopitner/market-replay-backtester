import pandas as pd
import numpy as np
from pathlib import Path

REQUIRED = {"timestamp", "open", "high", "low", "close", "volume"}

def load_bars(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    if df["timestamp"].duplicated().any():
        raise ValueError("Data contains duplicate timestamps.")
    if not df["timestamp"].is_monotonic_increasing:
        raise ValueError("Timestamps must be strictly monotonically increasing.")
    
    num_cols = ["open", "high", "low", "close", "volume"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="raise")
        if not np.isfinite(df[col]).all():
            raise ValueError(f"Non-finite values found in {col}.")
    
    if (df["high"] < df["low"]).any():
        raise ValueError("High price cannot be lower than low price.")
    if (df["high"] < df["open"]).any() or (df["high"] < df["close"]).any():
        raise ValueError("High price must be >= open and close.")
    if (df["low"] > df["open"]).any() or (df["low"] > df["close"]).any():
        raise ValueError("Low price must be <= open and close.")
        
    return df.reset_index(drop=True)