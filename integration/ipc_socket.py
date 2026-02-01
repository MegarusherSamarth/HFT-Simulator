# Socket-based IPC communication between Python ML strategies and the C++ HFT engine.
# Provides a lightweight communication layer using UPD sockets.

import socket
import json

class IPCSocket:
    def __init__(self, host: str = "127.0.0.1", market_port: int = 9000, signal_port: int = 9001):
        self.host = host
        self.market_port = market_port
        self.signal_port = signal_port
        
    def send_market_tick(self, tick: dict):
        # Send market tick data to the C++ engine.
        # Tick format: {"symbol": "BTCUSDT", "price": 42000.5, "quantity": 0.25}
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = json.dumps(tick).encode("utf-8")
            sock.sendto(message, (self.host, self.market_port))
        print(f"[IPC] Market tick sent: {tick}")
        
    def send_trade_signal(self, signal: dict):
        # Send trade signal to the C++ engine.
        # Signal Format: {"action": "BUY", "symbol": "BTCUSDT", "quantity": 0.1}
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = json.dumps(signal).encode("utf-8")
            sock.sendto(message, (self.host, self.signal_port))
        print(f"[IPC] Trade signal sent: {signal}")
        
    def listen(self, port: int, callback):
        # Listen fro message from the C++ engine.
        # Callback: function to process received messages.
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
            sock.bind((self.host, port))
            print(f"[IPC] Listening on {self.host}:{port}")
            while True:
                data, addr = sock.recvfrom(4096)
                try:
                    message = json.loads(data.decode("utf-8"))
                    callback(message)
                except json.JSONDecodeError:
                    print(f"[ERROR] Failed to decode message: {data}")

# Example usage
if __name__ == "__main__":
    ipc = IPCSocket()

    # Send a sample tick
    ipc.send_market_tick({"symbol": "BTCUSDT", "price": 42000.5, "quantity": 0.25})

    # Send a sample trade signal
    ipc.send_trade_signal({"action": "BUY", "symbol": "BTCUSDT", "quantity": 0.1})

    # Example listener (prints messages from engine)
    def handle_message(msg):
        print(f"[ENGINE MSG] {msg}")

    # Uncomment to run listener (blocks execution)
    # ipc.listen(port=9100, callback=handle_message)