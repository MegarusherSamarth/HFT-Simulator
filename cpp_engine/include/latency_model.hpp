// Including gaurds, these are preprocessor directives that prevent multiple inclusions of the same header files. This avoids compilation errors from duplicate definitions.

#ifndef LATENCY_MODEL_HPP
#define LATENCY_MODEL_HPP

// Provides random number generation facilities needed for simulating variable latency
#include <random>
// Provides time utilities for handling time durations and points  
#include <chrono>
using namespace std;

// Creating class
class LatencyModel {
    public: 
    // Creating constructor with 2 parameters
    LatencyModel(int minDelayMicros, int maxDelayMicros);

    // Function that will simulate the actual delay, likely by making the thread sleep for a random duration. this would be used when you want to actually pause execution
    void simulateDelay();

    // Func that returns a simulated latency value without actually pausing. This would be used when you want to measure or log latency without blocking execution.
    double simulate();

    private:
    int minDelay;
    int maxDelay;

    // Random-Number Generator
    // mt19937 is the Mersenne Twister pseudo-random number generator.
    // Provides high-quality random numbers for latency simulation
    // More robust than simpler alternatives like rand()
    mt19937 rng;

    // Uniform Distribution
    // Creates a uniform distribution between minDelay and maxDelay
    // Ensures each latency value in the range is equally probable.
    // Will be initialized in the constructor with the min/max delay values
    uniform_int_distribution<int> dist;
};

#endif // Ends include gaurd




// In high-frequency trading, latency modeling is crucial because:

// Network delays between exchanges and trading systems affect strategy performance

// Order execution times vary based on market conditions

// Realistic latency simulation helps test strategies under various network conditions

// Typical HFT latencies range from microseconds to milliseconds

// This class provides the foundation for simulating these variable delays in your trading simulator.

