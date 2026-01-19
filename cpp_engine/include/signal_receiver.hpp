#ifndef SIGNAL_RECEIVER_HPP
#define SIGNAL_RECEIVER_HPP
#include <functional>
#include <string>
using namespace std;

struct TradeSignal {
    string signal;
    double price;
    int volume;
    string symbol;
};

class SignalReceiver {
    public:
    SignalReceiver(int port);
    // Synchronous Recieve Method
    TradeSignal receiveSignal();

    // Asynchronous Listen Method
    void listen(function<void(const TradeSignal&)> callback);

    private:
    // Socket File Descriptor
    int sockfd;
    // Data Buffer
    char buffer[1024];
};

#endif // SIGNAL_RECEIVER_HPP





// HFT Context Analysis:
// Signal Generation in HFT:

// Trading signals come from various sources:

// Quantitative models (statistical arbitrage, mean reversion)

// Machine learning algorithms

// Market microstructure patterns

// Cross-market arbitrage opportunities

// News/sentiment analysis

// Architecture Role:

// This class acts as the bridge between strategy engines and execution systems

// In complex HFT systems, multiple signal receivers might handle different strategies

// Signal prioritization and conflict resolution are important considerations

// Performance Requirements:

// Signal-to-execution latency must be minimized

// Typical requirements: microseconds to milliseconds

// Network protocol choice critical (UDP vs TCP trade-offs)