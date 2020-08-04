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

enum IeType
{
    UnDefined               = 0,
    Recovery                = 14,
    Teid                    = 16,
    GsnAddress              = 133,
    ExtensionHeaderTypeList = 141,
    PrivateExtension        = 255,
};

struct RecoveryIe
{
    std::uint8_t ieType_;
    std::uint8_t restartCounter_;
};

struct TeidIe
{
    std::uint8_t ieType_;
    std::uint32_t teid_;
};

#endif // GTPU_TYPES_TYPES_H
