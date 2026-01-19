cmake_minimum_required(VERSION 3.10)

project(HFT_Simulator)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable(hft_simulator
    src/main.cpp
    src/order_book.cpp
    src/trade_engine.cpp
    src/latency_model.cpp
    src/market_data.cpp
    src/signal_receiver.cpp
)

target_include_directories(hft_simulator PRIVATE include)

target_compile_options(hft_simulator PRIVATE -Wall -Wextra -pthread)

target_link_libraries(hft_simulator PRIVATE ws2_32 Threads::Threads)
