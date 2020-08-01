#include "GtpUHeader.h"


std::uint8_t GtpUHeader::getVersionNumber() const
{
    return (flagField_ & 0xE0) >> 4;
}

GtpUHeader::ProtocolType GtpUHeader::getProtocolType() const
{
    return static_cast<GtpUHeader::ProtocolType>((flagField_ & ProtocolTypeFlag) >> 4);
}

GtpUHeader::GtpUHeader(IMessage::MessageType type)
    : messageType_(type)
{

}

GtpUHeader::~GtpUHeader()
{

}

void GtpUHeader::setExtentionFlag(bool enabled)
{
    if (enabled)
    {
        flagField_ |= ExtentionFlag;
    }
    else
    {
        flagField_ &= ~ExtentionFlag;
    }
}

void GtpUHeader::setSequenceFlag(bool enabled)
{
    if (enabled)
    {
        flagField_ |= SequenceFlag;
    }
    else
    {
        flagField_ &= ~SequenceFlag;
    }
}

void GtpUHeader::setPduNumberFlag(bool enabled)
{
    if (enabled)
    {
        flagField_ |= PduNumberFlag;
    }
    else
    {
        flagField_ &= ~PduNumberFlag;
    }
}

void GtpUHeader::setProtocolType()
{
    flagField_ |= ProtocolTypeFlag;
}
