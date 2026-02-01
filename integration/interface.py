# Python interface to C++ engine
# Provides a clean API for strategies to interact with the backend.

import subprocess
import socket
import json
from pathlib import Path

# Default Configuration
ENGINE_EXECUTABLE = Path(__file__).resolve().parent.parent / "cpp_engine" / "src" / "hft_simulator.exe"
MARKET_DATA_PORT = 9000
SIGNAL_PORT = 9001

class HFTInterface:
    def __init__(self, engine_path: Path = ENGINE_EXECUTABLE):
        self.engine_path = engine_path
        self.engine_process = None
    
    def start_engine(self):
        # Launched the compiled C++ engine as a subprocess.
        if not self.engine_path.exists():
            raise FileNotFoundError("HFT Engine Not Found at {self.engine_path}")
        self.engine_process = subprocess.Popen([str(self.engine_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[INFO] HFT engine started at {self.engine_path}")
        
    def stop_engine(self):
        # Terminate the C++ engine subprocess.
        if self.engine_process:
            self.engine_process.terminate()
            self.engine_process.wait()
            print("[INFO] HFT engine stopped.")
        
    def send_market_tick(self, tick: dict):
        # Sends market tick data to the C++ engine via UDP.
        # Tick Format: {"symbol": "BTCUSDT", "price": 42000.5, "quantity": 0.25}
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = json.dumps(tick).encode("utf-8")
        sock.sendto(message, ("127.0.0.1", MARKET_DATA_PORT))
        sock.close()
        print(f"[DEBUG] Market tick sent: {tick}")
        
    def send_trade_signal(self, signal: dict):
        # Sends trade signal to the C++ engine via UDP.
        # Signal Format: {"action": "BUY", "symbol": "BTCUSDT", "quantity": 0.1}
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = json.dumps(signal).encode("utf-8")
        sock.sendto(message, ("127.0.0.1", SIGNAL_PORT))
        sock.close()
        print(f"[DEBUG] Trade signal sent: {signal}")
        
    def read_engine_output(self):
        # Reads stdout from the C++ engine process (non-blocking).
        if self.engine_process and self.engine_process.stdout:
            for line in self.engine_process.stdout:
                print(f"[ENGINE] {line.decode().strip()}")


# Example Usage
if __name__ == "__main__":
    interface = HFTInterface()
    interface.start_engine()

    # Send a sample tick
    interface.send_market_tick({"symbol": "BTCUSDT", "price": 42000.5, "quantity": 0.25})

    # Send a sample trade signal
    interface.send_trade_signal({"action": "BUY", "symbol": "BTCUSDT", "quantity": 0.1})

    # Read engine output
    interface.read_engine_output()

    interface.stop_engine()