# Real-time feed emulator

import pandas as pd
import time
import socket
import json

class MarketDataStreamer:
    def __init__(self, data_path, interval_ms=100):
        self.data = pd.read_csv(data_path)
        # Convert to seconds
        self.interval = interval_ms / 1000.0 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # C++ engine listener
        self.target = ("localhost", 9999) 
        
    def stream(self):
        for _, row in self.data.iterrows():
            tick = {
                "timestamp" : row["timestamp"],
                "symbol" : row["symbol"],
                "price" : row["price"],
                "volume" : row["volume"]
            }
            message = json.dumps(tick).encode("utf-8")
            self.sock.sendto(message, self.target)
            time.sleep(self.interval)
    
if __name__ == "__main__":
    streamer = MarketDataStreamer("raw_data/btc_usdt.csv", interval_ms=100)
    streamer.stream()
