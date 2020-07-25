#ifndef GTPU_UDPSERVER_H
#define GTPU_UDPSERVER_H

#include <boost/asio.hpp>
#include <cstdlib>
#include <iostream>
#include <vector>

using boost::asio::ip::udp;

// Transmitting incomming/outgoing messages.
class UdpServer
{
public:
  UdpServer(boost::asio::io_context& io_context, const udp::endpoint& endpoint);

private:
  void setupReader();
  void onRead(const boost::system::error_code& error, size_t bytes_transferred);

private:
  udp::socket       socket_;
  udp::endpoint     endpoint_;
  std::vector<char> buffer_;
};

#endif // GTPU_UDPSERVER_H
