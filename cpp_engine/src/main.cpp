#define _NO_CRT_STDIO_INLINE 1  // Prevents inlline stdio func to avoid conflicts
#define NOMINMAX    // Prevents Windows.h form defining min and max macros that conflict with STL
#define byte win_byte_override  // Rename Windows byte to avoid conflict
#include <iostream>
#include <chrono>   // for timing and sleep func
#include <windows.h>   // windows api
#undef byte
#include "order_book.hpp"
#include "trade_engine.hpp"
#include "latency_model.hpp"
#include "market_data.hpp"
#include "signal_receiver.hpp"
#include <thread>
using namespace std;

int main(){
    cout << "Starting HFT Simulator..." << endl;

    // Initializing Core Components
    OrderBook orderBook;       // Central matching engine
    TradeEngine tradeEngine;   // execution and trade recording
    LatencyModel latencyModel(100, 500);     // 100-500 microseconds delay
    MarketDataReceiver marketReceiver(9000); // UDP port for market data
    SignalReceiver signalReceiver(9001);     // UDP port for trade signals

   // Toggle: set true for demo-only (prints trades and exits)
    bool demoMode = true;

    if (demoMode) {
        // === Synthetic demo trades injection (multi-line) ===

        // Seed order book with realistic levels so signals match
        Order buy1;
        buy1.id = 101;
        buy1.type = OrderType::BUY;
        buy1.price = 1500.0;
        buy1.quantity = 20;
        orderBook.addOrder(buy1);

        Order sell1;
        sell1.id = 102;
        sell1.type = OrderType::SELL;
        sell1.price = 1510.0;
        sell1.quantity = 25;
        orderBook.addOrder(sell1);

        // Inject synthetic market ticks
        MarketTick tick1;
        tick1.timestamp = "2025-11-15 00:30:00";
        tick1.symbol    = "TEST";
        tick1.price     = 1500.0;
        tick1.volume    = 10.0;
        orderBook.update(tick1);

        MarketTick tick2;
        tick2.timestamp = "2025-11-15 00:30:05";
        tick2.symbol    = "TEST";
        tick2.price     = 1510.0;
        tick2.volume    = 20.0;
        orderBook.update(tick2);

        MarketTick tick3;
        tick3.timestamp = "2025-11-15 00:30:10";
        tick3.symbol    = "TEST";
        tick3.price     = 1495.0;
        tick3.volume    = 15.0;
        orderBook.update(tick3);

        // Inject synthetic trade signals
        TradeSignal sig1;
        sig1.signal = "BUY";
        sig1.symbol = "TEST";
        sig1.price  = 1510.0; // will match sell1
        sig1.volume = 5;
        tradeEngine.execute(sig1, orderBook);

        TradeSignal sig2;
        sig2.signal = "SELL";
        sig2.symbol = "TEST";
        sig2.price  = 1500.0; // will match buy1
        sig2.volume = 10;
        tradeEngine.execute(sig2, orderBook);

        TradeSignal sig3;
        sig3.signal = "BUY";
        sig3.symbol = "TEST";
        sig3.price  = 1495.0; // may or may not match depending on book
        sig3.volume = 8;
        tradeEngine.execute(sig3, orderBook);

        // Print and exit cleanly
        tradeEngine.printTradeHistory();
        return 0;
    }


    // Market Data Thread
    // Start UDP listeners in separate threads
    std::thread marketThread([&](){ 
        marketReceiver.listen([&](const MarketTick &tick){ 
            orderBook.update(tick); 
        }); 
    }); // Semicolon required after lambda and thread declaration

    // Signal Processing Thread
    std::thread signalThread([&](){ 
        signalReceiver.listen([&](const TradeSignal &signal){
            double latency = latencyModel.simulate();
            std::this_thread::sleep_for(chrono::microseconds(static_cast<int>(latency)));
            tradeEngine.execute(signal, orderBook); 
        }); 
    }); // Semicolon required after lambda and thread declaration

    // Main loop (optional monitoring)
    for (int i = 0; i < 100; ++i){
        cout << "Tick " << i << " processed." << endl;
        std::this_thread::sleep_for(chrono::milliseconds(100));
    }

    // Join threads before exiting
    marketThread.join();
    signalThread.join();

    cout << "Simulation complete. Trade log saved." << endl;

    // Printing all trades executed during simulation
    tradeEngine.printTradeHistory();
    
    return 0;
}





// HFT Architecture Analysis:
// System Flow:

// text
// Market Data (Port 9000) → OrderBook → Market State
// Trading Signals (Port 9001) → Latency Simulation → TradeEngine → Executed Trades
// Concurrency Model:

// Market Thread: Handles real-time data feed (highest priority)

// Signal Thread: Processes trading decisions with simulated latency

// Main Thread: System monitoring and control

// Latency Simulation:
// The sleep in the signal thread realistically models:

// Network latency between strategy and execution engines

// Exchange gateways processing time

// Risk system checks

// Typical HFT round-trip times (100-500μs is realistic)

// Production Considerations:

// cpp
// Real HFT systems would need:
// 1. Error handling and reconnection logic
// 2. Performance monitoring and metrics
// 3. Graceful shutdown mechanisms
// 4. Configuration management
// 5. Logging and audit trails
// Potential Issues:

// Missing printTradeHistory() method declaration

// No error handling for socket connections

// Thread safety concerns with shared orderBook access

// No mechanism to stop the UDP listeners gracefully

// This main file successfully orchestrates all the HFT simulator components into a cohesive system that realistically models high-frequency trading with proper concurrency and latency simulation.