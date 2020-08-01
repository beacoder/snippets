#include "GtpuHeader.h"


std::uint8_t GtpuHeader::getVersionNumber() const
{
    return (flags_ & 0xE0) >> 4;
}

GtpuHeader::ProtocolType GtpuHeader::getProtocolType() const
{
    return static_cast<GtpuHeader::ProtocolType>((flags_ & ProtocolTypeFlag) >> 4);
}

GtpuHeader::GtpuHeader(IMessage::MessageType type)
    : messageType_(type)
{

}

GtpuHeader::~GtpuHeader()
{

}

void GtpuHeader::setExtensionFlag(bool enabled)
{
    if (enabled)
    {
        flags_ |= ExtensionFlag;
    }
    else
    {
        flags_ &= ~ExtensionFlag;
    }
}

void GtpuHeader::setSequenceFlag(bool enabled)
{
    if (enabled)
    {
        flags_ |= SequenceFlag;
    }
    else
    {
        flags_ &= ~SequenceFlag;
    }
}

void GtpuHeader::setPduNumberFlag(bool enabled)
{
    if (enabled)
    {
        flags_ |= PduNumberFlag;
    }
    else
    {
        flags_ &= ~PduNumberFlag;
    }
}

void GtpuHeader::setProtocolType()
{
    flags_ |= ProtocolTypeFlag;
}
