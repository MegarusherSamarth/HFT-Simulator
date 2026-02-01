# Loads a trained LSTM model and generates predictions on live or historical market data.
# Outputs signals that can be consumed by execute_strategy.py.

import torch
import torch.nn as nn
import numpy as np
from pathlib import Path
from python_strategies.training.train_lstm import LSTMModel
from data_feed.live_data_loader import LiveDataLoader 

# Path to saved model
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "lstm_model.pt"


class LSTMModel(nn.Module):
    def __init__(self, input_size=2, hidden_size=64, num_layers=2, output_size=3):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # last time step
        return torch.softmax(out, dim=1)  # 3-class probabilities


class LSTMPredictor:
    def __init__(self, model_path=MODEL_PATH, window_size=20):
        self.model = LSTMModel(input_size=2)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
        self.model.eval()
        self.window_size = window_size
        self.buffer = []  # Rolling Window of ticks
        print(f"[INFO] Loaded LSTM model from {model_path}")

    def preprocess(self, tick): 
        # Append tick to buffer and prepare sequence.
        self.buffer.append([tick["price"], tick["volume"]]) 
        if len(self.buffer) < self.window_size: 
            return None 
        seq = np.array(self.buffer[-self.window_size:], dtype=np.float32) 
        return torch.tensor(seq, dtype=torch.float32).unsqueeze(0) 
    
    def predict(self, tick): 
        # Run inference on live tick stream.
        seq = self.preprocess(tick) 
        if seq is None: 
            return None 
        with torch.no_grad(): 
            probs = self.model(seq).squeeze().numpy()  # [p_sell, p_hold, p_buy]
            signal = int(np.argmax(probs))             # 0, 1, or 2
        print(f"[LSTM] Tick={tick} | Probs={probs} | Signal={signal}") 
        return signal


# Example live integration 
if __name__ == "__main__": 
    predictor = LSTMPredictor() 
    
    def handle_tick(tick): 
        predictor.predict(tick) 
    
    loader = LiveDataLoader(symbol="btcusdt") 
    loader.register_callback(handle_tick) 
    loader.start() 
    
    import time
    time.sleep(10)
    loader.stop()
    print("[INFO] Stopped after 10 seconds")
