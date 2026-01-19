// Pybind11 bindings
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "order_book.hpp"
#include "trade_engine.hpp"
#include "latency_model.hpp"
#include "market_data.hpp"
using namespace std;

namespace py = pybind11;

PYBIND11_MODULE(hft_engine, m) {
    m.doc() = "Python bindings for the C++ HFT Simulator engine.";

    // Bind Order Struct
    py::class_<Order>(m, "Order")
        .def(py::init<int, double, int>(), py::arg("id"), py::arg("price"), py::arg("quantity"))
        .def_readwrite("id", &Order::id)
        .def_readwrite("price", &Order::price)
        .def_readwrite("quantity", &Order::quantity);

    // Bind OrderBook
    py::class_<OrderBook>(m, "OrderBook")
        .def(py::init<>())
        .def("update", &OrderBook::update)
        .def("get_best_bid", &OrderBook::getBestBid)
        .def("get_best_ask", &OrderBook::getBestAsk);

    // Bind TradeEngine
    py::class_<TradeEngine>(m, "TradeEngine")
        .def(py::init<>())
        .def("process_trade", &TradeEngine::processTrade)
        .def("get_trade_history", &TradeEngine::getTradeHistory);

    // Bind LatencyModel
    py::class_<LatencyModel>(m, "LatencyModel")
        .def(py::init<int, int>(), py::arg("min_us"), py::arg("max_us"))
        .def("simulate", &LatencyModel::simulate);

    // Bind MarketTick struct
    py::class_<MarketTick>(m, "MarketTick")
        .def_readwrite("symbol", &MarketTick::symbol)
        .def_readwrite("price", &MarketTick::price)
        .def_readwrite("quantity", &MarketTick::quantity);

    // Bind MarketDataReceiver (optional, usually socket-based)
    py::class_<MarketDataReceiver>(m, "MarketDataReceiver")
        .def(py::init<int>(), py::arg("port"))
        .def("listen", &MarketDataReceiver::listen);
}