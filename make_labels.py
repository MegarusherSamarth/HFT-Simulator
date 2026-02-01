import pandas as pd
import numpy as np

def make_labels(csv_path, threshold=0.00001):
    """
    Reads a CSV with price/volume columns and generates labels:
    0 = SELL, 1 = HOLD, 2 = BUY
    threshold = relative change (%) to decide HOLD zone
    """
    df = pd.read_csv(csv_path)

    prices = df["price"].values
    labels = []

    for i in range(1, len(prices)):
        delta = (prices[i] - prices[i-1]) / prices[i-1]

        if delta > threshold:
            labels.append(2)  # BUY
        elif delta < -threshold:
            labels.append(0)  # SELL
        else:
            labels.append(1)  # HOLD

    # Align labels with dataframe length
    df = df.iloc[1:].copy()
    df["label"] = labels

    # Print distribution
    unique, counts = np.unique(labels, return_counts=True)
    dist = dict(zip(unique, counts))
    print("[INFO] Label distribution:")
    print(df["label"].value_counts())


    # Save new CSV with labels
    out_path = csv_path.replace(".csv", "_labeled.csv")
    df.to_csv(out_path, index=False)
    print(f"[INFO] Saved labeled dataset to {out_path}")

    return out_path

if __name__ == "__main__":
    # Run from project root
    make_labels("data_feed/raw_data/btc_usdt.csv", threshold=0.00001)
