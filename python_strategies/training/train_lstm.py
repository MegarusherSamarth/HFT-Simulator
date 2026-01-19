import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from pathlib import Path

# Dataset
class TickDataset(Dataset):
    def __init__(self, df, window_size=20):
        # df must contain columns: price, volume
        # window_size: number of timestamps per sequence
        self.data = df[["price", "volume"]].values
        self.window = window_size
        
    def __len__(self):
        return len(self.data) - self.window
    
    def __getitem__(self, idx):
        x = self.data[idx : idx + self.window]
        next_price = self.data[idx + self.window][0]
        current_price = self.data[idx + self.window - 1][0] # Price delta
        y = 1.0 if next_price > current_price else 0.0
        
        return (torch.tensor(x, dtype = torch.float32), torch.tensor([y], dtype = torch.float32))
    
# LSTM Model
class LSTMModel(nn.Module):
    def __init__(self, input_size=2, hidden_size=64, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size = input_size,
            hidden_size = hidden_size,
            num_layers = num_layers,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return torch.sigmoid(out)

# Training Function
def train_model(csv_path, model_path):
    df = pd.read_csv(csv_path)
    dataset = TickDataset(df)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    model = LSTMModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.BCELoss()
    
    print("[INFO] Starting LSTM training...")
    
    for epoch in range(10):
        total_loss = 0.0
        
        for x, y in loader:
            optimizer.zero_grad()
            output = model(x)
            loss = loss_fn(output, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"[EPOSH {epoch+1}/10], Loss: {total_loss: .4f}")
        
    torch.save(model.state_dict(), model_path)
    print(f"[INFO] Model saved to {model_path}")

# Main
import sys

if __name__ == "__main__":
    # Use arguments if provided, else fall back to defaults
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data_feed/raw_data/btc_usdt.csv"
    model_path = sys.argv[2] if len(sys.argv) > 2 else "python_strategies/models/lstm_model.pt"

    train_model(csv_path, model_path)
    print(f"[INFO] Training complete. Model saved at {model_path}")
