# Generates evaluation reports for trading strategies using metrics.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from python_strategies.utils.metrics import Metrics
# from python_strategies.evaluation.metrics import Metrics

class BacktestReport:
    def __init__(self, prices, actions, returns = None, signals= None):
        # prices: list/array of prices
        # actions: list/array of actions (0=BUY, 1=SELL, 2=HOLD)
        self.prices = prices
        self.actions = actions
        self.returns = returns
        self.signals = signals
        
    def generate_report(self):
        # Compute trading metrics and return dictionary.
        report = {
            "PnL": Metrics.calculate_pnl(self.prices, self.actions),
            "Sharpe Ratio": Metrics.sharpe_ratio(self.returns) if self.returns is not None else None,
            "Win Rate": Metrics.win_rate(self.prices, self.actions),
            "Accuracy": Metrics.accuracy(self.signals, self.actions) if self.signals is not None else None
        }
        return report
    
    def plot_equity_curve(self, save_path=None):
        # Plot cumulative PnL curve.
        equity = []
        cumulative = 0.0
        position = None
        entry = None
        
        for price, action in zip(self.prices, self.actions):
            if action == 0: # BUY
                position = "LONG"
                entry = price
            elif action == 1 and position == "LONG":
                cumulative += price - entry
                position = None
            equity.append(cumulative)
            
        plt.figure(figsize=(10, 5))
        plt.plot(equity, label = "Equity Curve", color="blue")
        plt.title("Backtest Equity Curve")
        plt.xlabel("Trade Index")
        plt.ylabel("Cumulative PnL")
        plt.legend()
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()


# Example
if __name__ == "__main__":
    prices = [100, 102, 101, 105, 103, 107]
    actions = [0, 2, 2, 1, 0, 1]  # BUY, HOLD, SELL, BUY, SELL
    returns = [0.02, -0.01, 0.04, -0.02, 0.03]   # demo returns
    signals = [1, 0, 1, 1, 0, 1]                 # demo predictions or labels

    report = BacktestReport(prices, actions, returns=returns, signals=signals)
    metrics = report.generate_report()
    print("Backtest Report: ", metrics)
    
    report.plot_equity_curve()
    