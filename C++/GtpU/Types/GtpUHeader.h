#ifndef GTPU_TYPES_GTPUHEADER_H
#define GTPU_TYPES_GTPUHEADER_H

#include "Interfaces/IMessage.h"
#include <cstdint>


class GtpuHeader
{
public:
    enum ProtocolType
    {
        GTP_Prime = 0,
        GTP       = 1,
    };

    enum HeaderFlag
    {
        PduNumberFlag    = 0x01,
        SequenceFlag     = 0x02,
        ExtentionFlag    = 0x04,
        ProtocolTypeFlag = 0x10,
    };

    GtpuHeader(IMessage::MessageType type);
    ~GtpuHeader();

    std::uint8_t  getVersionNumber() const;
    ProtocolType  getProtocolType() const;

private:
    void setExtentionFlag(bool enabled);
    void setSequenceFlag(bool enabled);
    void setPduNumberFlag(bool enabled);
    void setProtocolType();

private:

// 3GPP TS 29.281
// Figure 5.1-1: Outline of the GTP-U Header
//
//                                        Bits
// Octets	8	7	6	5	4	3	2	1
// 1		     Version            PT	(*)	E	S	PN
// 2		Message Type
// 3		Length (1st Octet)
// 4		Length (2nd Octet)
// 5		Tunnel Endpoint Identifier (1st Octet)
// 6		Tunnel Endpoint Identifier (2nd Octet)
// 7		Tunnel Endpoint Identifier (3rd Octet)
// 8		Tunnel Endpoint Identifier (4th Octet)
// 9		Sequence Number (1st Octet)
// 10		Sequence Number (2nd Octet)
// 11		N-PDU Number
// 12		Next Extension Header Type

    std::uint8_t  flags_;
    std::uint8_t  messageType_;
    std::uint16_t length_;
    std::uint32_t teid_;
    std::uint16_t sequenceNbr_;
    std::uint8_t  nPduNbr_;
    std::uint8_t  extensionType_;
};

#endif // GTPU_TYPES_GTPUHEADER_H
