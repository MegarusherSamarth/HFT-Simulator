#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <thread>
#include <cstring>
#include "signal_receiver.hpp"
// #include <argparse/inet.h>
#include <unistd.h>
#include <nlohmann/json.hpp>
#include <functional>
using namespace std;
using json = nlohmann::json;

SignalReceiver::SignalReceiver(int port)
{
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    sockaddr_in servaddr{};
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr));
}

TradeSignal SignalReceiver::receiveSignal(){
    sockaddr_in cliaddr{};
    socklen_t len = sizeof(cliaddr);
    int bytes = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&cliaddr, &len);

    TradeSignal ts;

    if (bytes <= 0) {
        cerr << "[WARNING] No data received from UDP socket, skipping signal." << endl;
        ts.signal = "NONE";
        ts.price = 0.0;
        ts.volume = 0.0;
        return ts;
    }

    string raw(buffer, bytes);
    cout << "[DEBUG] Raw buffer: " << raw << endl;

    json msg = json::parse(raw, nullptr, false); 

    if (msg.is_discarded()) {
        cerr << "[ERROR] Invalid JSON received, skipping signal." << endl;
        ts.signal = "NONE";
        ts.price = 0.0;
        ts.volume = 0.0;
        return ts;
    }

    ts.signal = msg.value("signal", "NONE");
    ts.price  = msg.value("price", 0.0);
    ts.volume = msg.value("volume", 0.0);

    return ts;
}


void SignalReceiver::listen(std::function<void(const TradeSignal&)> callback) {
    std::thread([this, callback]() {
        int count = 0;
        while (count < 5) {
            TradeSignal signal = receiveSignal();
            callback(signal);
            count++;
        }
    }).detach();
}