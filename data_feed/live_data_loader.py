# Streams live tick data from Binance for multiple pairs.
# Provides ticks in dict format for ML Strategies and lightweight live metrics.

import json
import websocket
import threading
import time
from collections import deque
import matplotlib.pyplot as plt
import pandas as pd
import os, sys
import numpy as np

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class LiveDataLoader:
    def __init__(self, symbols=None):
        if symbols is None:
            symbols = ["btcusdt", "ethusdt", "solusdt"]
        self.symbols = [s.lower() for s in symbols]
        self.ws = None
        self.callbacks = []

    def _on_message(self, ws, message):
        data = json.loads(message)

        # Combined streams wrap payload in "data"
        payload = data.get("data", data)

        tick = {
            "symbol": payload["s"],       # e.g. BTCUSDT
            "price": float(payload["p"]), # trade price
            "volume": float(payload["q"]),# trade volume
            "timestamp": float(payload["T"])
        }

        for cb in self.callbacks:
            cb(tick)

    def _on_error(self, ws, error):
        print(f"[ERROR] WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("[INFO] WebSocket closed")

    def _on_open(self, ws):
        print("[INFO] WebSocket connection established")

    def start(self):
        # Build combined stream URL
        streams = "/".join([f"{s}@trade" for s in self.symbols])
        url = f"wss://stream.binance.com:9443/stream?streams={streams}"

        self.ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open,
        )
        thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        thread.start()

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def stop(self):
        if self.ws:
            self.ws.close()


# === Example usage with lightweight live metrics ===
if __name__ == "__main__":
    # Separate buffers per symbol
    windows = {sym.upper(): deque(maxlen=50) for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]}
    equity_curves = {sym.upper(): [] for sym in windows}
    actions_logs = {sym.upper(): [] for sym in windows}
    tick_counter = {sym.upper(): 0 for sym in windows}

    def live_callback(tick):
        sym = tick["symbol"]
        tick_counter[sym] += 1
        windows[sym].append((tick["price"], tick["volume"]))

        if len(windows[sym]) == windows[sym].maxlen:
            df = pd.DataFrame(list(windows[sym]), columns=["price", "volume"])

            returns = df["price"].pct_change().dropna()
            pnl = returns.sum()
            sharpe = (returns.mean() / returns.std()) * np.sqrt(len(returns)) if returns.std() != 0 else None
            win_rate = (returns > 0).mean()

            equity_curves[sym].append(pnl)
            actions_logs[sym].append("BUY" if returns.iloc[-1] > 0 else "SELL")

            sharpe_str = f"{sharpe:.3f}" if sharpe is not None else "N/A"

            # Print every 10 ticks per symbol
            if tick_counter[sym] % 10 == 0:
                print(f"[{sym}] Price = {tick['price']:.2f} | Volume = {tick['volume']:.6f} | "
                      f"Action = {actions_logs[sym][-1]} | PnL={pnl:.6f} | Sharpe = {sharpe_str} | WinRate = {win_rate:.2%}")

    loader = LiveDataLoader(symbols=["btcusdt", "ethusdt", "solusdt"])
    loader.register_callback(live_callback)
    loader.start()

    # Run for 1 minute
    time.sleep(60)
    loader.stop()
    print("[INFO] Stopped after 60 seconds.")

    # Plot equity curves for each symbol
    plt.figure(figsize=(10, 6))
    for sym, curve in equity_curves.items():
        if curve:
            plt.plot(curve, label=f"{sym} Equity Curve")
    plt.legend()
    plt.title("Live Equity Curves (BTC, ETH, SOL)")
    plt.xlabel("Ticks")
    plt.ylabel("PnL")
    plt.show()
