# Streams live tick data from an exchange API (Eg: NSE/BSE, NASDAQ, Binance).
# Provides ticks in dict format for ML Strategies.

import json
import websocket
import threading
import time

class LiveDataLoader:
    def __init__(self, symbol= "btcusdt", interval = "1s"):
        # symbol: trading pair (Eg: btcusdt, nse/bse, ethusdt)
        # interval: tick interval (default 1s)
        
        self.symbol = symbol.lower()
        self.interval = interval
        self.ws = None
        self.callbacks = []
        
    def _on_message(self, ws, message):
        data = json.loads(message)
        tick = {
            "symbol": self.symbol.upper(),
            "price": float(data["p"]),  # trade prices
            "volume": float(data["q"]),  # trade volume
            "timestamp": float(data["T"]),  # trade time
        }
        
        # Notify all registered callbacks
        for cb in self.callbacks:
            cb(tick)
    
    def _on_error(self, ws, error):
        print(f"[ERROR] WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg): 
        print("[INFO] WebSocket closed") 
    
    def _on_open(self, ws): 
        print("[INFO] WebSocket connection established") 
    
    def start(self):
        # Start streaming live data.
        url = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"
        self.ws = websocket.WebSocketApp(
            url,
            on_message = self._on_message,
            on_error = self._on_error,
            on_close = self._on_close,
            on_open = self._on_open,
        )
        
        # Run WebSocket in background thread
        thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        thread.start()
        
    def register_callback(self, callback):
        # Register a callback to recieve ticks.
        self.callbacks.append(callback)
        
    def stop(self):
        if self.ws:
            self.ws.close()
            
# Example
if __name__ == "__main__":
    def print_tick(tick):
        print("[TICK]", tick)
    
    loader = LiveDataLoader(symbol="btcusdt")
    loader.register_callback(print_tick)
    loader.start()
    
    # Keep alive for demo
    import time
    time.sleep(10)
    loader.stop()
    print("[INFO] Stopped after 10 seconds")