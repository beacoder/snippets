#include "UdpServer.h"

UdpServer::UdpServer(boost::asio::io_context& io_context, const udp::endpoint& endpoint)
    : socket_(io_context, endpoint)
    , endpoint_(endpoint)
{
    setupReader();
}

void UdpServer::setupReader()
{
    udp::endpoint remoteEndpoint;
    socket_.async_receive_from(boost::asio::buffer(buffer_), remoteEndpoint, onRead);
}

void UdpServer::onRead(const boost::system::error_code& error, size_t bytesRead)
{
    if (error) {
        std::cout << "Receive failed: " << error.message() << std::endl;
        return;
    }

    std::cout << "Received: '" << std::string(buffer_.begin(), buffer_.begin()+bytesRead)
              << "' (" << error.message() << ")" << std::endl;
}

// void UdpServer::do_send(std::size_t length)
// {
//     socket_.async_send_to(
//         boost::asio::buffer(data_, length), sender_endpoint_,
//         [this](boost::system::error_code /*ec*/, std::size_t /*bytes_sent*/)
//         {
//             do_receive();
//         });
// }

// int main(int argc, char* argv[])
// {
//     try
//     {
//         if (argc != 2)
//         {
//             std::cerr << "Usage: async_udp_echo_server <port>\n";
//             return 1;
//         }

//         boost::asio::io_context io_context;

//         UdpServer s(io_context, std::atoi(argv[1]));

//         io_context.run();
//     }
//     catch (std::exception& e)
//     {
//         std::cerr << "Exception: " << e.what() << "\n";
//     }

//     return 0;
// }
