import pandas as pd
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# Import your LSTM model
from python_strategies.training.train_lstm import LSTMModel, TickDataset

def backtest_model(csv_path, model_path):
    df = pd.read_csv(csv_path)
    window_size = 20

    # Load trained model
    model = LSTMModel()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    actions = []
    pnl = 0.0
    equity_curve = [0.0]
    wins = 0
    total_trades = 0

    # Simple backtest loop
    for i in range(len(df) - window_size - 1):
        seq = df[["price", "volume"]].iloc[i:i+window_size].values
        state = torch.tensor(seq, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            pred = model(state)
        action = torch.argmax(pred).item()
        actions.append(action)

        # Debug first few predictions
        if i < 5:
            print(f"Step {i}, Pred={pred.numpy()}, Action={action}")

        # Trading logic: BUY=2, SELL=0, HOLD=1
        next_price = df["price"].iloc[i+window_size]
        current_price = df["price"].iloc[i+window_size-1]

        if action == 2:  # BUY
            trade_return = (next_price - current_price) / current_price
            pnl += trade_return
            total_trades += 1
            if trade_return > 0:
                wins += 1
        elif action == 0:  # SELL
            trade_return = (current_price - next_price) / current_price
            pnl += trade_return
            total_trades += 1
            if trade_return > 0:
                wins += 1
        # HOLD does nothing

        equity_curve.append(pnl)

    from collections import Counter
    print("[INFO] Action Distribution: ", Counter(actions))
    
    # Metrics
    sharpe = None
    if len(equity_curve) > 1:
        returns = np.diff(equity_curve)
        if returns.std() != 0:
            sharpe = returns.mean() / returns.std()

    win_rate = wins / total_trades if total_trades > 0 else 0.0
    accuracy = sum([1 for a in actions if a in [0,2]]) / len(actions) 

    report = {
        "PnL": round(pnl, 4),
        "Sharpe Ratio": sharpe,
        "Win Rate": round(win_rate, 4),
        "Accuracy": accuracy,
        "equity_curve": equity_curve,
        "actions": actions
    }

    print("LSTM Backtest Report:", report)

    # Plot equity curve
    plt.figure(figsize=(8,4))
    plt.plot(equity_curve, label="Equity Curve", color="blue")
    plt.xlabel("Trade Index")
    plt.ylabel("Cumulative PnL")
    plt.title("Backtest Equity Curve")
    plt.legend()
    plt.grid(True)
    plt.show()

    return report

if __name__ == "__main__":
    csv_path = "data_feed/raw_data/btc_usdt.csv"
    model_path = "python_strategies/models/lstm_model.pt"
    backtest_model(csv_path, model_path)
