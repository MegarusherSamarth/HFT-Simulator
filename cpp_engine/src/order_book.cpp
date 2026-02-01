#include "order_book.hpp"
#include "market_data.hpp"
#include <iostream>
#include <algorithm>
using namespace std;

OrderBook::OrderBook(){}

void OrderBook::addOrder(const Order& order){
    orderLookup[order.id] = order;

    if (order.type == OrderType::BUY){
        buyOrders[order.price].push_back(order);
    } else {
        sellOrders[order.price].push_back(order);
    }
    matchOrders();
}

void OrderBook::cancelOrder(int orderId){
    if (orderLookup.find(orderId) == orderLookup.end()) return;

    Order order = orderLookup[orderId];

    if (order.type == OrderType::BUY) {
        auto& ordersAtPrice = buyOrders[order.price];
        ordersAtPrice.erase(
            remove_if(ordersAtPrice.begin(), ordersAtPrice.end(), [orderId](const Order& o){
                return o.id == orderId;
            }), ordersAtPrice.end()
        );
        if (ordersAtPrice.empty()) buyOrders.erase(order.price);
    } else {
        auto& ordersAtPrice = sellOrders[order.price];
        ordersAtPrice.erase(
            remove_if(ordersAtPrice.begin(), ordersAtPrice.end(), [orderId](const Order& o ){
                return o.id == orderId;
            }), ordersAtPrice.end()
        );

        if (ordersAtPrice.empty()) sellOrders.erase(order.price);
    }

    orderLookup.erase(orderId);
}

void OrderBook::matchOrders(){
    while (!buyOrders.empty() && !sellOrders.empty()) {
        auto buyIt = buyOrders.begin();
        auto sellIt = sellOrders.begin();

        double buyPrice = buyIt->first;
        double sellPrice = sellIt->first;

        if (buyPrice < sellPrice) break;

        Order& buyOrder = buyIt->second.front();
        Order& sellOrder = sellIt->second.front();

        int tradeQty = min(buyOrder.quantity, sellOrder.quantity);
        executeTrade(buyOrder, sellOrder);

        buyOrder.quantity -= tradeQty;
        sellOrder.quantity -= tradeQty;

        if (buyOrder.quantity == 0){
            buyIt->second.erase(buyIt->second.begin());
            orderLookup.erase(buyOrder.id);

            if (buyIt->second.empty()) buyOrders.erase(buyIt);
        }

        if (sellOrder.quantity == 0) {
            sellIt->second.erase (sellIt->second.begin());
            orderLookup.erase(sellOrder.id);

            if (sellIt->second.empty()) sellOrders.erase(sellIt);
        }
    }
}

void OrderBook::executeTrade (const Order& buy, const Order& sell) {
    cout << "Trade Executed: BUY " << buy.id << " and SELL " << sell.id << " at price " << sell.price << " for quantity " << min(buy.quantity, sell.quantity) << endl;
}

vector<Order> OrderBook::getBuyOrders() const {
    vector<Order> result;

    for (const auto& [price, orders] : buyOrders){
        result.insert(result.end(), orders.begin(), orders.end());
    }
    return result;
}

vector<Order> OrderBook::getSellOrders() const {
    vector<Order> result;

    for (const auto& [price, orders]:sellOrders){
        result.insert(result.end(), orders.begin(), orders.end());
    }
    return result;
}

void OrderBook::update(const MarketTick& tick) {
    Order synthetic;
    synthetic.id = -1;
    synthetic.type = OrderType::SELL; // or BUY based on your logic
    synthetic.price = tick.price;
    synthetic.quantity = static_cast<int>(tick.volume);

    addOrder(synthetic);
}