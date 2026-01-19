#include "trade_engine.hpp"
#include "signal_receiver.hpp"
#include <iostream>
#include <chrono>
#include <ctime>
#include <cstring>
using namespace std;

TradeEngine::TradeEngine() {}

void TradeEngine::processTrade(const Order& buy, const Order& sell){
    int tradeQty = min(buy.quantity, sell.quantity);
    double tradePrice = sell.price; // Assume sell price is execution price

    Trade trade = {
        buy.id, sell.id, tradePrice, tradeQty, getCurrentTimestamp()
    };

    tradeHistory.push_back(trade);

    cout << "[TRADE] BUY " << buy.id << " <-> SELL " << sell.id << " || Price: " << tradePrice << " | Qty: " << tradeQty << " | Time: " << trade.timestamp << endl;
}

const vector<Trade>& TradeEngine::getTradeHistory() const {
    return tradeHistory;
}

void TradeEngine::printTradeHistory() const {
    cout << "\n=== Trade History ===" << endl;
    for (const auto& trade : tradeHistory) {
        cout << "BuyID: " << trade.buyOrderId
             << " | SellID: " << trade.sellOrderID
             << " | Price: " << trade.price
             << " | Qty: " << trade.quantity
             << " | Time: " << trade.timestamp << endl;
    }
}


string TradeEngine::getCurrentTimestamp() const {
    auto now = chrono::system_clock::now();
    time_t timeNow = chrono::system_clock::to_time_t(now);
    char buffer[26];
    // ctime_s(buffer, sizeof(buffer), &timeNow);
    strncpy(buffer, ctime(&timeNow), sizeof(buffer));
    buffer[sizeof(buffer) - 1] = '\0';  // Ensure null-termination

    // Remove newline character from ctime output
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len - 1] == '\n') {
        buffer[len - 1] = '\0';
    }
    
    return string(buffer);
}

void TradeEngine::execute(const TradeSignal& signal, const OrderBook& book) {
    vector<Order> candidates;

    if (signal.signal == "BUY") {
        candidates = book.getSellOrders(); // Match against sell side
    } else if (signal.signal == "SELL") {
        candidates = book.getBuyOrders(); // Match against buy side
    } else {
        cerr << "[WARN] Unknown signal type: " << signal.signal << endl;
        return;
    }

    int remainingQty = signal.volume;

    for (const Order& order : candidates) {
        if (remainingQty <= 0) break;

        if ((signal.signal == "BUY" && signal.price >= order.price) ||
            (signal.signal == "SELL" && signal.price <= order.price)) {

            Order synthetic;
            synthetic.id = -1; // synthetic signal order
            synthetic.type = (signal.signal == "BUY") ? OrderType::BUY : OrderType::SELL;
            synthetic.price = signal.price;
            synthetic.quantity = min(order.quantity, remainingQty);

            if (signal.signal == "BUY") {
                processTrade(synthetic, order);
            } else {
                processTrade(order, synthetic);
            }

            remainingQty -= synthetic.quantity;
        }
    }

    if (remainingQty > 0) {
        cout << "[INFO] Signal partially filled. Remaining qty: " << remainingQty << endl;
    }
}
