# Transforms raw market ticks into ML-ready feature vectors.
# Used by noth LSTM training and RL agent training.

import numpy as np
import pandas as pd

class FeatureEngineer:
    def __init__(self, window: int = 20):
        # :param window: Number of past ticks to compute rolling features.
        self.window = window
        
    def add_returns(self, df: pd.DataFrame):
        # Add to returns.
        df["log_return"] = np.log(df["price"] / df["price"].shift(1))
        df["log_return"].fillna(0, inplace=True)
        return df
    
    def add_volatility(self, df: pd.DataFrame):
        # Rolling volatility
        df["volatility"] = df["log_return"].rolling(self.window).std()
        df["volatility"].fillna(0, inplace=True)
        return df
    
    def add_volume_pressure(self, df: pd.DataFrame):
        # Volume pressure = buy_volume - sell_volume
        # If your dataset doesn't have buy/sell split, approximate using price movement.
        df["volume_pressure"] = np.where(
            df["price"].diff() > 0,
            df["quantity"],
            -df["quantity"]
        )
        return df
    
    def add_price_change(self, df: pd.DataFrame):
        # Simple price delta.
        df["price_change"] = df["price"].diff().fillna(0)
        return df
    
    def normalize(self, df: pd.DataFrame, columns=None):
        # Min-max normalization.
        if columns is None:
            columns = ["price", "quantity", "log_return", "volatility", "volume_pressure", "price_change"]
        
        for col in columns:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                df[col] = (df[col] - min_val) / (max_val - min_val + 1e-9)
            
        return df
    
    def build_features(self, df: pd.DataFrame):
        # Full feature pipeline.
        # Input: Raw dataframe with columns [timestamp, price, quantity]
        # Output: ML-ready dataframe with engineered features.
        df = df.copy()
        
        df = self.add_returns(df)
        df = self.add_volatility(df)
        df = self.add_volume_pressure(df)
        df = self.add_price_change(df)
        df = self.normalize(df)
        
        return df
    
    def to_sequences(self, df: pd.DataFrame, seq_len: int = 20):
        # Convert dataframe into LSTM sequences.
        # Returns X (features) and y (labels).
        
        feature_cols = ["price", "quantity", "log_return", "volatility", "volume_pressure", "price_change"]
        
        X, y = [], []
        data = df[feature_cols].values
        labels = (df["price"].shift(-1) > df["price"]).astype(int).values # 1 = upward
        
        for i in range(len(df) - seq_len - 1):
            X.append(data[i:i + seq_len])
            y.append(labels[i + seq_len])
            
        return np.array(X), np.array(y)
    
# Example Usage
if __name__ == "__main__":
    # Load sample data
    df = pd.DataFrame({
        "timestamp": [1, 2, 3, 4, 5],
        "price": [100, 101, 102, 101, 103],
        "quantity": [1.2, 0.8, 1.5, 1.1, 0.9]
    })

    fe = FeatureEngineer(window=3)
    df_features = fe.build_features(df)
    print(df_features)

    X, y = fe.to_sequences(df_features, seq_len=3)
    print("X shape:", X.shape)
    print("y shape:", y.shape)