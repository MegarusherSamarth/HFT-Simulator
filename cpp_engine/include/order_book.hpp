#ifndef ORDER_BOOK_HPP
#define ORDER_BOOK_HPP
#include "market_data.hpp"
#include <map>
#include <vector>
#include <string>
#include <functional>
using namespace std;

enum class OrderType { BUY, SELL };

struct Order {
    int id;
    OrderType type;
    double price;
    int quantity;
};

// The core matching engine that maintains buy/sell orders and executes trades.
class OrderBook {
    public:
    OrderBook();

    // Order Addition
    // Adds a new order to the appropriate side of the book. Critical HFT operation - must be optimized for speed. In real systems, this would be microseconds-sensitive
    void addOrder(const Order& order);

    // Order Cancellations
    // Removes an order from the book by its ID. Essential for HFT strategies that frequently update positions. Low-Latency cancellation is crucial for risk management.
    void cancelOrder(int orderId);

    // Matching Engine
    // Core func that finds and execute possible trades. Compares buy and sell orders to find matching prices. In continuous trading, this runs whenever new orders arrive.
    void matchOrders();

    // Book Inspection
    // Returns current state of buy/sell sides for display or analysis. const indicates these don't modify the order book. Useful for strategy decision-making and GUI display.
    vector<Order> getBuyOrders() const;
    vector<Order> getSellOrders() const;

    // Market Data Integration
    // Updates order book based on incoming market data. could represent market-driven changes or implied orders. essential for keeing simulated book in sync with market.
    void update(const MarketTick& tick);

    private:
    // Buy orders storage
    map<double, vector<Order>, greater<double>> buyOrders; // Highest Price First
    // Sell orders storage
    map<double, vector<Order>> sellOrders; // Lowest Price First
    // Order lookup table
    // Provides O(log n) access to orders by ID for cancellation. essential for efficient order management. maintains a secondary index into the price-level maps.
    map<int, Order> orderLookup;

    // Trade Execution
    void executeTrade(const Order& buy, const Order& sell);
};

#endif 






// HFT Context Analysis:
// Order Book Importance:

// The order book is the heart of any electronic trading system

// HFT strategies make decisions based on book depth and imbalance

// Microsecond-level performance is critical in real systems

// Matching Logic:

// Price-time priority is standard in most electronic markets

// Buy orders match when buy price >= sell price

// The greater<double> comparator efficiently implements bid-side priority

// Performance Considerations for Real HFT:

// map provides O(log n) operations but may be too slow for ultra-HFT

// Real systems often use custom data structures or arrays

// Memory allocation (vectors growing) can introduce latency spikes

// Lock-free structures needed for multi-threaded access

// Trading Protocol:

// This implements continuous matching (like stock exchanges)

// Alternative: auction-based matching (like opening/closing crosses)

// Real systems handle partial fills, iceberg orders, and complex order types

// This order book provides the fundamental matching engine that will drive your HFT simulator's trading logic and price discovery.