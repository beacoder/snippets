#ifndef GTPU_TYPES_TYPES_H
#define GTPU_TYPES_TYPES_H

#include <cstdint>


using UdpPort       = std::uint16_t;
using PdcpPduNumber = std::uint16_t;

struct LongPdcpPduNumber
{
    std::uint32_t pdcpPduNumber_;
    std::uint16_t padding_;
};

struct ServiceClassIndicator
{
    std::uint8_t sci_;
    std::uint8_t padding_;
};

#endif // GTPU_TYPES_TYPES_H
