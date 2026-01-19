#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <thread>
#include <cstring>
#include "market_data.hpp"
// #include <arpa/inet.h>
#include <unistd.h>
#include <nlohmann/json.hpp> // JSON parsing library (needs to installed)
#include <functional>
using namespace std;

using json = nlohmann::json;

MarketDataReceiver::MarketDataReceiver(int port)
{
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    sockaddr_in servaddr{};
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr));
}

MarketTick MarketDataReceiver::receiveTick() {
    sockaddr_in cliaddr{};
    socklen_t len = sizeof(cliaddr);
    int bytes = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&cliaddr, &len);

    MarketTick mt;

    if (bytes <= 0) {
        cerr << "[WARNING] No data received from UDP socket, skipping tick." << endl;
        mt.timestamp = "invalid";
        mt.symbol = "N/A";
        mt.price = 0.0;
        mt.volume = 0.0;
        return mt;
    }

    string raw(buffer, bytes);
    cout << "[DEBUG] Raw buffer: " << raw << endl;

    json tick = json::parse(raw, nullptr, false); // ✅ no exceptions

    if (tick.is_discarded()) {
        cerr << "[ERROR] Invalid JSON received, SKIPPING "<< endl;
        mt.timestamp = "invalid";
        mt.symbol = "N/A";
        mt.price = 0.0;
        mt.volume = 0.0;
        return mt;
    }

    mt.timestamp = tick.value("timestamp", "invalid");
    mt.symbol = tick.value("symbol", "N/A");
    mt.price = tick.value("price", 0.0);
    mt.volume = tick.value("volume", 0.0);

    return mt;
}


void MarketDataReceiver::listen(std::function<void(const MarketTick&)> callback) {
    std::thread([this, callback]() {
        int count = 0;
        while (count < 5) {
            MarketTick tick = receiveTick();
            callback(tick);
            count++;
        }
    }).detach();
}
