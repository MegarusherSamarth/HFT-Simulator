# Data Cleaning

import pandas as pd

def preprocess_tick_data(input_path, output_path):
    df = pd.read_csv(input_path)
    
    # Basic Cleaning
    df.dropna(inplace=True)
    df = df.rename(columns= {
        "time" : "timestamp",
        "symbol" : "symbol",
        "price" : "price",
        "qty" : "volume"
    })
    
    # Optional: filter for specific symbol or time range
    df = df[df["symbol"] == "BTCUSDT"]
    
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    preprocess_tick_data("raw_data/raw_ticks.csv", "raw_data/btc_usdt.csv")