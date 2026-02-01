import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from pathlib import Path
from collections import Counter
import sys
import random

# Dataset
class TickDataset(Dataset):
    def __init__(self, df, window_size=20, threshold=0.001, inject_hold=False):
        self.data = df[["price", "volume"]].values
        self.window = window_size
        self.threshold = threshold
        self.inject_hold = inject_hold
        
    def __len__(self):
        return len(self.data) - self.window
    
    def __getitem__(self, idx):
        x = self.data[idx : idx + self.window]
        next_price = self.data[idx + self.window][0]
        current_price = self.data[idx + self.window - 1][0]
        delta = (next_price - current_price) / current_price
        
        if delta > self.threshold:
            y = 2  # BUY
        elif delta < -self.threshold:
            y = 0  # SELL
        else:
            y = 1  # HOLD

        # Optional synthetic HOLD injection for balance
        if self.inject_hold and random.random() < 0.1:
            y = 1

        return (torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.long))

# LSTM Model
class LSTMModel(nn.Module):
    def __init__(self, input_size=2, hidden_size=64, num_layers=2, output_size=3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        out = self.fc(hn[-1])
        return out

# Auto-balance threshold finder
def find_balanced_threshold(df, window_size=20, start=0.00001, end=0.001, step=0.00001):
    for th in [start + i*step for i in range(int((end-start)/step))]:
        dataset = TickDataset(df, window_size=window_size, threshold=th)
        labels = [dataset[i][1].item() for i in range(len(dataset))]
        dist = Counter(labels)
        if len(dist) == 3:  # all classes present
            print(f"[INFO] Balanced threshold found: {th}, distribution={dist}")
            return th
    print("[WARN] No balanced threshold found, falling back to synthetic HOLD injection")
    return start

# Training Function
def train_model(csv_path, model_path):
    df = pd.read_csv(csv_path)

    # Try to auto-balance threshold
    threshold = find_balanced_threshold(df, window_size=20)
    dataset = TickDataset(df, window_size=20, threshold=threshold, inject_hold=True)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    labels = [dataset[i][1].item() for i in range(len(dataset))]
    print("[INFO] Final Label Distribution:", Counter(labels))

    model = LSTMModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss(weight=torch.tensor([1.0, 0.5, 1.0]))

    print("[INFO] Starting LSTM training...")

    num_epochs = 50
    for epoch in range(num_epochs):
        total_loss = 0.0
        for x, y in loader:
            optimizer.zero_grad()
            output = model(x)
            loss = loss_fn(output, y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"[EPOCH {epoch+1}/{num_epochs}], Loss: {total_loss/len(loader): .4f}")

    torch.save(model.state_dict(), model_path)
    print(f"[INFO] Model saved to {model_path}")

# Main
if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data_feed/raw_data/btc_usdt.csv"
    model_path = sys.argv[2] if len(sys.argv) > 2 else "python_strategies/models/lstm_model.pt"
    train_model(csv_path, model_path)
    print(f"[INFO] Training complete. Model saved at {model_path}")
