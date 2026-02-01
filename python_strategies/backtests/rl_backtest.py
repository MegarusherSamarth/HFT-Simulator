import torch
import pandas as pd
import numpy as np
from pathlib import Path
from python_strategies.training.train_rl_agent import RLTrainer  # ensure class name matches your train_rl_agent.py
from python_strategies.evaluation.backtest_report import BacktestReport

def backtest_model(csv_path=None, model_path=None):
    # Default paths
    if model_path is None:
        model_path = Path(__file__).resolve().parents[1] / "models" / "rl_agent.pt"
    if csv_path is None:
        csv_path = Path(__file__).resolve().parents[2] / "data_feed" / "raw_Data" / "btc_usdt.csv"

    # Load trained RL agent
    agent = RLTrainer()
    agent.model.load_state_dict(torch.load(model_path))
    agent.model.eval()

    # Load dataset
    df = pd.read_csv(csv_path)
    prices = df["price"].values
    volumes = df["volume"].values

    # Generate actions using RL agent
    actions = []
    for i in range(len(df)):
        state = np.array([prices[i], volumes[i]], dtype=np.float32)
        action = agent.choose_action(state)
        actions.append(action)

    # Run backtest
    report = BacktestReport(prices, actions)
    metrics = report.generate_report()
    print("RL Agent Backtest Report:", metrics)
    report.plot_equity_curve()

    # Return metrics + equity curve + actions for comparison scripts
    # metrics["equity_curve"] = report.equity_curve
    metrics["actions"] = actions
    return metrics

if __name__ == "__main__":
    backtest_model()
