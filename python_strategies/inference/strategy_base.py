# Abstract base class for trading strategies.
# Provides a unified interface for ML-driven strategies to interact with the HFT engien.

from abc import ABC, abstractmethod
from integration.execute_strategy import StrategyExecutor

class StrategyBase(ABC):
    # Base class for all trading strategies.
    # Subclasses must implement the 'predict' method to generate signals.
    
    def __init__(self, symbol: str = "BTCUSDT", use_interface: bool = True):
        self.symbol = symbol
        self.executor = StrategyExecutor(use_interface= use_interface)
        
    @abstractmethod
    def predict(self, tick: dict) -> float:
        # Abstract method to geenrate a prediction from a tick.
        # Must return a float between 0 and 1 (probability of upward move).
        pass
    
    def run(self, tick: dict):
        # Execute strategy on a single tick.
        # Calls predict() -> converts to signal -> sends to engine.
        prob = self.predict(tick)
        self.executor.execute(prob)
        
    def shutdown(self):
        # Clean up resources (stop engine if needed).
        self.executor.shutdown()
        
# Example Subclass
class RandomStrategy(StrategyBase):
    # Demo strategy that generates random predictions.
    # Useful for testing the pipeline.

    import random

    def predict(self, tick: dict) -> float:
        return self.random.random()  # random probability between 0 and 1


# Example usage
if __name__ == "__main__":
    # Demo tick
    tick = {"symbol": "BTCUSDT", "price": 42000.5, "quantity": 0.25}

    # Run random strategy
    strategy = RandomStrategy()
    strategy.run(tick)
    strategy.shutdown()