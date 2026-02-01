import matplotlib.pyplot as plt
from collections import Counter
from python_strategies.backtests.lstm_backtest import backtest_model as lstm_backtest
from python_strategies.backtests.rl_backtest import backtest_model as rl_backtest

def print_comparison_table(lstm_report, rl_report):
    def safe_fmt(value):
        if value is None:
            return "—"
        if isinstance(value, float):
            return f"{value:.4f}"
        return str(value)

    print("\n=== Metrics Comparison Table ===")
    print(f"{'Model':<10}{'PnL':<15}{'Sharpe':<15}{'Win Rate':<15}{'Accuracy':<15}")
    print("-" * 70)
    print(f"{'LSTM':<10}{safe_fmt(lstm_report['PnL']):<15}{safe_fmt(lstm_report['Sharpe Ratio']):<15}{safe_fmt(lstm_report['Win Rate']):<15}{safe_fmt(lstm_report['Accuracy']):<15}")
    print(f"{'RL':<10}{safe_fmt(rl_report['PnL']):<15}{safe_fmt(rl_report['Sharpe Ratio']):<15}{safe_fmt(rl_report['Win Rate']):<15}{safe_fmt(rl_report['Accuracy']):<15}")


def compare_backtests():
    csv_path = "data_feed/raw_data/btc_usdt.csv"
    lstm_model_path = "python_strategies/models/lstm_model.pt"

    print("\n[INFO] Running LSTM Backtest...")
    lstm_report = lstm_backtest(csv_path, lstm_model_path)

    print("\n[INFO] Running RL Backtest...")
    rl_report = rl_backtest(csv_path)

    # Print metrics in table format 
    print_comparison_table(lstm_report, rl_report) 
    # Print action distributions 
    print("\n=== Action Distributions ===") 
    print("[INFO] LSTM Actions:", Counter(lstm_report["actions"])) 
    print("[INFO] RL Actions:", Counter(rl_report["actions"]))

    # Plot only LSTM equity curve (RL curve not available in Option 2)
    plt.figure(figsize=(8,4))
    plt.plot(lstm_report["equity_curve"], label="LSTM", color="blue")
    plt.xlabel("Trade Index")
    plt.ylabel("Cumulative PnL")
    plt.title("Backtest Comparison (LSTM vs RL)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    compare_backtests()
