#ifndef MARKET_DATA_HPP
#define MARKET_DATA_HPP

// Provides func objects and callbacks, essential for event-driven market data handling
#include <functional>
// Provides string handling utilities for symbol names and timestamps
#include <string>
using namespace std;

struct MarketTick {
    string timestamp;
    string symbol;
    double price;
    double volume;
};

class MarketDataReceiver {
    public:
    MarketDataReceiver(int port);

    // Synchronous Recieve Method
    // Blocks and returns a single MarketTick
    // Useful for polling-based approaches or simple simulations
    // In real HFT, this would be too slow - async approaches are preferred.
    MarketTick receiveTick();

    // Asynchronous Listen Method
    // Takes a callback function as parameter.
    // Will call the provided func whenever new market data arrives.
    // Critical for HFT: this enables event-driven, low-latency provessing.
    // The callback revcieves a const MarketTick&.
    void listen(function<void(const MarketTick&)> callback);

    private:
    //     Socket File Descriptor:
    // Stores the network socket connection
    // Typical Unix/Linux socket programming pattern
    // Used to receive UDP or TCP market data packets
    int sockfd;

    //     Data Buffer
    // Fixed-size buffer for receiving raw network data
    // 1024 bytes is a common size for network buffers
    // In real HFT systems, buffers might be optimized for specific exchange protocols
    char buffer[1024];
};

#endif // MARKET_DATA_HPP






// HFT Context Analysis:
// Market Data in HFT:

// Market data feeds are the lifeblood of HFT strategies

// Typical volumes: Thousands to millions of messages per second

// Low-latency parsing is critical (microsecond matters)

// Common protocols: FIX/FAST, OUCH, proprietary binary formats

// Architecture Implications:

// The callback pattern (listen method) is essential for real HFT systems

// Synchronous receiveTick() is likely for testing/simulation

// Real systems would use non-blocking I/O and ring buffers

// The fixed buffer size suggests this is a simplified implementation

// Potential Enhancements for Real HFT:

// Multiple sockets for different data feeds

// Memory pooling for MarketTick objects to avoid allocation delays

// Lock-free data structures for thread-safe callback handling

// Hardware timestamping support

// Protocol-specific optimizations

// This interface provides the foundation for receiving and processing market data, which is the first step in any HFT trading pipeline.