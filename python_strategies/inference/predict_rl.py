# Loads a trained RL agent and generates BUY / SELL / HOLD signals on tick data.

import torch
import numpy as np
from pathlib import Path
from python_strategies.training.train_rl_agent import QNetwork
from data_feed.live_data_loader import LiveDataLoader

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "rl_agent.pt"

class RLPredictor:
    def __init__(self, model_path = MODEL_PATH):
        self.model = QNetwork()
        self.model.load_state_dict(torch.load(model_path, map_location= torch.device("cpu")))
        self.model.eval()
        print(f"[INFO] Loaded RL agent from {model_path}")
        
    def preprocess(self, tick: dict):
        return torch.tensor([tick["price"], tick["volume"]], dtype=torch.float32)
    
    def predict(self, tick: dict) -> int:
        # Run inference on a single tick.
        # Returns action: 0 = BUY, 1= SELL, 2= HOLD
        state = self.preprocess(tick)
        with torch.no_grad():
            q_values = self.model(state)
            action = torch.argmax(q_values).item()
        print(f"[PREDICT] Tick={tick} | Action={action}")
        return action
    
# Example
if __name__ == "__main__":
    predictor = RLPredictor()
    
    def handle_tick(tick): 
        predictor.predict(tick) 
    
    loader = LiveDataLoader(symbol="btcusdt") 
    loader.register_callback(handle_tick) 
    loader.start() 
    
    import time
    time.sleep(10)
    loader.stop()
    print("[INFO] Stopped after 10 seconds")