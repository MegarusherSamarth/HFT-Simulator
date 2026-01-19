#ifndef TRADE_ENGINE_HPP
#define TRADE_ENGINE_HPP
// For recieving trading signals from strategies
#include "signal_receiver.hpp"
// For accessing market state and order matching
#include "order_book.hpp"
#include <vector>
#include <string>
using namespace std;

struct Trade {
    int buyOrderId;
    int sellOrderID;
    double price;
    int quantity;
    string timestamp;
};

class TradeEngine {
    public:
    TradeEngine();
    
    // Trade Processing
    // Records a completed trade between a buy and sell order
    // Typically called by the OrderBook when orders match
    // Adds the trade to history and likely triggers: Position updates, P&L calculations, Risk management checks, execution reports
    void processTrade(const Order& buy, const Order& sell);

    // Trade History Access
    // Returns a const reference to the complete trade history
    // const ensures the history cannot be modified externally
    // Used for: Reporting and analytics, GUI display, Strategy performance analysis, Regulatory reporting
    const vector<Trade>& getTradeHistory() const;

    // Signal Execution
    // Core HFT method: converts trading signals into actual orders
    // Takes a trading signal and current market state.
    // Implementations execution logic: Market orders vs limit orders, sizing calculations, risk checks, timing decisions
    // Critical for strategy performance - poor execution can negate alpha
    void execute(const TradeSignal& signal, const OrderBook& book);
    void printTradeHistory() const;
    
    private:
    // Trade History Storage
    vector<Trade> tradeHistory;
    // Timestamp utility
    string getCurrentTimestamp() const;
};

#endif // TRADE_ENGINE_HPP




// HFT Context Analysis:
// Trade Engine Role:

// text
// Signals → Trade Engine → Orders → Order Book → Trades → Trade Engine
//     ↑                                      ↓
// Strategy                             Position Updates & P&L
// Execution Logic:
// The execute method is where strategy meets reality. It must handle:

// Order Type Selection: Market vs limit orders

// Sizing: Full execution vs partial fills

// Timing: Immediate vs scheduled execution

// Risk Checks: Position limits, credit checks

// Market Impact: Avoiding price movement from large orders

// Performance Considerations:

// Trade processing must be extremely fast (microseconds)

// History storage should not block execution thread

// Timestamp generation needs nanosecond precision in real HFT