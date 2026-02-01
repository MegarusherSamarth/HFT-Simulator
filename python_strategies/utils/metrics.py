# Centralized metrics for ML models and trading performance.
# Used by LSTM training, RL training, and strategy evaluation.

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
)

class Metrics:
    # Classification Metrics (LSTM)
    @staticmethod
    def classification_metrics(y_true, y_pred):
        y_pred_binary = (np.array(y_pred) > 0.5).astype(int)
        return {
            "accuracy": accuracy_score(y_true, y_pred_binary),
            "precision": precision_score(y_true, y_pred_binary, zero_division=0),
            "recall": recall_score(y_true, y_pred_binary, zero_division=0),
            "f1_score": f1_score(y_true, y_pred_binary, zero_division=0),
        }

    # Regression Metrics
    @staticmethod
    def regression_metrics(y_true, y_pred):
        return {
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "mae": mean_absolute_error(y_true, y_pred),
        }

    # Trading Metrics (Strategy Performance)
    @staticmethod
    def calculate_pnl(prices, actions):
        pnl = 0.0
        position = 0
        entry_price = 0.0
        for price, action in zip(prices, actions):
            if action == 0 and position == 0:  # BUY
                position = 1
                entry_price = price
            elif action == 1 and position == 1:  # SELL
                pnl += price - entry_price
                position = 0
        return pnl

    @staticmethod
    def win_rate(prices, actions):
        wins = 0
        total = 0
        position = 0
        entry_price = 0.0
        for price, action in zip(prices, actions):
            if action == 0 and position == 0:  # BUY
                position = 1
                entry_price = price
            elif action == 1 and position == 1:  # SELL
                total += 1
                if price > entry_price:
                    wins += 1
                position = 0
        return wins / total if total > 0 else 0.0

    @staticmethod
    def sharpe_ratio(returns, risk_free_rate=0.0):
        excess_returns = np.array(returns) - risk_free_rate
        if excess_returns.std() == 0:
            return 0.0
        return excess_returns.mean() / excess_returns.std()

    @staticmethod
    def max_drawdown(equity_curve):
        equity = np.array(equity_curve)
        if len(equity) == 0:
            return 0.0
        peak = np.maximum.accumulate(equity)
        # Avoid Divide by 0
        with np.errstate(divide='ignore', invalid='ignore'):
            drawdown = np.where(peak > 0, (equity - peak) / peak, 0.0)
        return drawdown.min()

    @staticmethod
    def trading_report(prices, actions):
        pnl = Metrics.calculate_pnl(prices, actions)
        winrate = Metrics.win_rate(prices, actions)

        # Build equity curve
        equity = []
        cumulative = 0.0
        position = None
        entry = None
        for price, action in zip(prices, actions):
            if action == 0:  # BUY
                position = "LONG"
                entry = price
            elif action == 1 and position == "LONG":  # SELL
                cumulative += price - entry
                position = None
            equity.append(cumulative)

        sharpe = Metrics.sharpe_ratio(np.diff(equity) if len(equity) > 1 else [0])
        mdd = Metrics.max_drawdown(equity)

        return {
            "PnL": pnl,
            "Win Rate": winrate,
            "Sharpe Ratio": sharpe,
            "Max Drawdown": mdd,
        }
    
    @staticmethod
    def accuracy(y_true, y_pred):
        y_pred = np.array(y_pred)
        # Agar predictions float/probability hain (0.0–1.0), threshold lagao
        if y_pred.dtype.kind in {'f'} and ((y_pred > 1).any() == False):
            y_pred_binary = (y_pred > 0.5).astype(int)
            return accuracy_score(y_true, y_pred_binary)
        # Agar already integer/binary hain (0/1), direct compare
        return accuracy_score(y_true, y_pred)



# Example Usage
if __name__ == "__main__":
    y_true = [1, 0, 1, 1]
    y_pred = [0.8, 0.3, 0.9, 0.4]
    print("Classification:", Metrics.classification_metrics(y_true, y_pred))

    prices = [100, 102, 101, 105, 103]
    actions = [0, 2, 2, 1, 2]  # BUY, HOLD, HOLD, SELL
    print("Trading Report:", Metrics.trading_report(prices, actions))
