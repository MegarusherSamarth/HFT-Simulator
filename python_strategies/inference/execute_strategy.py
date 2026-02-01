# Executes ML-driven trading strategies by sending signals to the C++ HFT engine.
# Uses IPC (via interface.py or ipc_socket.py) to communicate with the backend.

import random
import time
from integration.interface import HFTInterface
# Alternatively, you can use IPCSocket:
# from integration.ipc_socket import IPCSocket

class StrategyExecutor:
    def __init__(self, use_interface: bool = True):
        if use_interface:
            self.bridge = HFTInterface()
            self.bridge.start_engine()
        else:
            from integration.ipc_socket import IPCSocket
            self.bridge = IPCSocket()
    
    def generate_signal(self, prediction: float, symbol: str = "BTCUSDT"):
        # Convert ML prediction into a trade signal.
        # :param prediction: Model output (e.g., probability of upward move.)
        # :param symbol: Trading symbol.
        # :return: Trade signal dict.
        
        action = "BUY" if prediction > 0.5 else "SELL"
        quantity = round(random.uniform(0.01, 0.1), 4)   # Demo Quantity
        signal = {"action": action, "symbol": symbol, "quantity": quantity}
        return signal
    
    def execute(self, prediction: float):
        # Send trade signal to engine based on prediction.
        signal = self.generate_signal(prediction)
        if isinstance(self.bridge, HFTInterface):
            self.bridge.send_trade_signal(signal)
        else:
            self.bridge.send_trade_signal(signal)
        print(f"[STRATEGY] Executed signal: {signal}")
        
    def shutdown(self):
        # Stop engine of using HFTInterface.
        if isinstance(self.bridge, HFTInterface):
            self.bridge.stop_engine()

# Example usage
if __name__ == "__main__":
    executor = StrategyExecutor(use_interface=True)

    # Simulate predictions from ML model
    predictions = [0.7, 0.3, 0.8, 0.2]

    for p in predictions:
        executor.execute(p)
        time.sleep(1)

    executor.shutdown()