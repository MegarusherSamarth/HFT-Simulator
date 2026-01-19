#include <thread>
#include <random>
#include <chrono>
#include "latency_model.hpp"
using namespace std;

// Constructor Implementation
LatencyModel::LatencyModel(int minDelayMicros, int maxDelayMicros) : minDelay(minDelayMicros), maxDelay(maxDelayMicros), rng(random_device{}()), dist(minDelayMicros, maxDelayMicros) {}

double LatencyModel::simulate() {
    int delay = dist(rng);
    std::this_thread::sleep_for(chrono::microseconds(delay));  // used to actually paue execution
    return static_cast<double>(delay); // return simulated latency
}


// minDelay(minDelayMicros): Initializes minDelay with provided min latency
// maxDealy(maxDelayMicros): Initializes maxDelay with provided max latency
// -- rng(random_device{}()): Critical HFT Component:
// -- random_device{}: creates a temporaru random_device object
// -- this seeds the Mersenne Twister (mt19937) with true randomness
// -- essential for non-deterministic simulation
// dist(minDelayMicros, maxDelayMicros): Initiales the uniform distribution with the min/max range.



// HFT Context Analysis:
// Latency in High-Frequency Trading:

// Typical Ranges:

// Co-located systems: 50-200 microseconds

// Same data center: 100-500 microseconds

// Cross-continental: 1-50 milliseconds

// Sources of Latency:

// Network propagation delays

// Exchange matching engine processing

// Order gateway processing

// Risk system checks

// Strategy computation time

// Implementation Quality:

// True Random Seeding: Using random_device prevents predictable patterns

// Mersenne Twister: High-quality PRNG suitable for simulation

// Uniform Distribution: Realistic for network latency modeling

// Microsecond Precision: Appropriate for HFT timescales

// Performance Considerations:

// The sleep_for call is appropriate for simulation but would never be used in real HFT

// Real HFT systems measure latency but don't artificially add it

// In production, you'd use high-resolution clocks to measure actual latency



// Real HFT Usage:
// In actual trading systems, latency modeling is used for:

// Backtesting: Simulating realistic execution delays

// Strategy Development: Testing under various network conditions

// Infrastructure Planning: Determining colocation requirements

// Performance Testing: Stress testing under worst-case latency scenarios

// This implementation provides a solid foundation for simulating the crucial timing aspects of high-frequency trading, allowing you to test how strategies perform under realistic latency conditions.