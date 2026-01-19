# Utility module for loading and preparing raw tick data.
# Used by LSTM training, RL training, and live inference pipelines.

import pandas as pd
from pathlib import Path

class DataLoader:
    def __init__(self, required_columns=None):
        # required_columns: list of columns that must exist in the CSV.
        if required_columns is None:
            required_columns = ["timestamp", "price", "volume"]
        
        self.required_columns = required_columns
    
    def load_csv(self, path: str | Path) -> pd.DataFrame:
        # Load a CSV file and validate required columns.
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")
        
        df = pd.read_csv(path)
        
        # Validate columns
        for col in self.required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
            
        # Sort by timestamp if present
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp").reset_index(drop=True)
        
        return df
    
    def downsample(self, df: pd.Dataframe, step: int = 1) -> pd.DataFrame:
        # Downsample tick data (e.g., take every Nth row).
        if step <= 1:
            return df
        return df.iloc[::step].reset_index(drop=True)
    
    def normalize(self, df: pd.DataFrame, columns=None) -> pd.DataFrame:
        # Min-Max noramlize selected columns.
        if columns is None:
            columns = ["price", "volume"]
        
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                df[col] = (df[col] - min_val) / (max_val - min_val + 1e-9)
            return df

# Example Usage
if __name__ == "__main__":
    loader = DataLoader()
    
    df = loader.load_csv("data_feed/raw_data/btc_usdt.csv")
    df = loader.downsample(df, step=2)
    df = loader.normalize(df)
    print(df.head())