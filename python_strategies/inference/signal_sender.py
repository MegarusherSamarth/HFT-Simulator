# Emulates trade signal generation and sends them to the C++ HFT engine via UDP.

import socket
import json
import random
import time

SIGNAL_PORT = 9001
HOST = "127.0.01"

class SignalSender:
    def __init__(self, host: str = HOST, port: int = SIGNAL_PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send_signal(self, action: str, symbol: str, quantity: float):
        # Send a trade signal to the C++ engine.
        # :param action: "BUY" or "SELL"
        # :param symbol: Trading symbol (e.g., "BTCUSDT")
        # :param quantity: Trade quantity
        
        signal = {"action": action, "symbol": symbol, "quantity": quantity}
        message = json.dumps(signal).encode("utf-8")
        self.sock.sendto(message, (self.host, self.port))
        print(f"[SIGNAL] Sent: {signal}")
        
    def random_signal(self, symbol: str = "BTCUSDT"):
        # Generate and send a random BUY/SELL signal.
        action = random.choice(["BUY", "SELL"])
        quantity = round(random.uniform(0.01, 0.2), 4)
        self.send_signal(action, symbol, quantity)
    
    def close(self):
        # Close the UDP socket.
        self.sock.close()
        
# Example usage
if __name__ == "__main__":
    sender = SignalSender()
    
    # Send 10 random signals with 1-second delay
    for i in range(10):
        sender.random_signal("BTCUSDT")
        time.sleep(1)
    
    sender.close()