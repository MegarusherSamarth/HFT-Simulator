# HFT Simulator & Secure E-Voting Evaluation Framework

## 📌 Overview
This project is a modular, audit‑ready simulator for **High‑Frequency Trading (HFT)** strategies and **secure e‑voting systems**.  
It is designed to showcase **scalable architecture, reproducible metrics, and demo‑ready outputs** for recruiters, panels, and technical reviewers.

Key highlights:
- ⚡ Modular C++/Python engine for trading simulations
- 📊 Automated reporting: PnL, Sharpe Ratio, Win Rate, Accuracy
- 🤖 Model benchmarking: LSTM vs Reinforcement Learning (RL) accuracy comparison
- 🔐 Secure e‑voting features with auditability and IP strategy mapping
- 🛠️ Automation‑first design: no manual variable definitions required in notebooks

---

## 🚀 Features
- **Backtest Engine**
  - Runs trading strategies over synthetic or real price feeds
  - Generates actions (`BUY`, `SELL`, `HOLD`) and signals

- **Evaluation Reports**
  - `BacktestReport` class computes metrics automatically
  - Accuracy charts for LSTM vs RL models
  - Equity curve plotting with Matplotlib

- **Metrics Module (`utils/metrics.py`)**
  - PnL calculation
  - Sharpe Ratio
  - Win Rate
  - Accuracy (signal vs action alignment)

- **Automation**
  - Wrapper functions (`evaluate_lstm`, `evaluate_rl`) run backtests and return metrics
  - No manual variable definitions in notebooks

---

## 📂 Project Structure
```
HFT-Simulator/
│
├── python_strategies/
│   ├── utils/
│   │   └── metrics.py
│   ├── evaluation/
│   │   └── backtest_report.py
│   ├── backtests/
│   │   ├── lstm_backtest.py
│   │   └── rl_backtest.py
│   └── ...
│
├── notebooks/
│   └── accuracy_chart.ipynb
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/HFT-Simulator.git
cd HFT-Simulator
pip install -r requirements.txt
```

---

## 📊 Usage

### Run LSTM Backtest
```python
from python_strategies.evaluation.backtest_report import evaluate_lstm

metrics = evaluate_lstm()
print(metrics)
```

### Run RL Backtest
```python
from python_strategies.evaluation.backtest_report import evaluate_rl

metrics = evaluate_rl()
print(metrics)
```

### Compare Accuracy
```python
import pandas as pd
import matplotlib.pyplot as plt

lstm_metrics = evaluate_lstm()
rl_metrics = evaluate_rl()

df = pd.DataFrame([
    {"Model": "LSTM", "Accuracy": lstm_metrics["Accuracy"]},
    {"Model": "RL", "Accuracy": rl_metrics["Accuracy"]}
])

df.set_index("Model")[["Accuracy"]].plot(kind="bar", color="orange")
plt.title("Model Accuracy Comparison")
plt.ylabel("Accuracy")
plt.ylim(0,1)
plt.show()
```

---

## 📈 Demo Outputs
- **Equity Curve**: cumulative PnL plotted over trades  
- **Accuracy Chart**: LSTM vs RL accuracy side‑by‑side  
- **Metrics Report**: dictionary with PnL, Sharpe, Win Rate, Accuracy  

---

## 🛡️ License
This project is licensed under the **MIT License** — simple, permissive, recruiter‑friendly.  
See the LICENSE file for details.

---

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

---

## 📬 Contact
Created by **MegarusherSamarth**  
Visionary technologist & systems architect  
For collaboration or recruiter demos, connect via LinkedIn or GitHub.
```
