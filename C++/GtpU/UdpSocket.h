#ifndef GTPU_UDPSOCKET_H
#define GTPU_UDPSOCKET_H

class UdpSocket
{
public:
    UdpSocket();
    ~UdpSocket();

    bind();

privat:
    uint32_t fd;
};

#endif // GTPU_UDPSOCKET_H
