# Metrics Calculations

import numpy as np

def calculate_metrics(df):
    pnl = df["pnl"].cumsum()
    returns = pnl.pct_change().fillna(0)
    sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) != 0 else 0
    drawdown = pnl.max() - pnl.min()
    
    return {
        "total_pnl" : pnl.iloc[-1],
        "sharpe" : sharpe,
        "drawdown" : drawdown
    }