#include "GtpUMessage.h"

IMessage::MessageId GtpUMessage::getMessageId() const
{
    return GtpU;
}

std::uint16_t GtpUMessage::getMessageType() const
{
    return messageType_;
}

std::uint8_t GtpUMessage::getVersionNumber() const
{
    return (fixedField_ & 0xE0) >> 4;
}

GtpUMessage::ProtocolType GtpUMessage::getProtocolType() const
{
    return static_cast<GtpUMessage::ProtocolType>((fixedField_ & 0x10) >> 4);
}

GtpUMessage::GtpUMessage()
{

}

GtpUMessage::~GtpUMessage()
{

}

void GtpUMessage::setExtentionFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= 0x04;
    }
    else
    {
        fixedField_ &= ~0x04;
    }
}

void GtpUMessage::setSequenceFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= 0x02;
    }
    else
    {
        fixedField_ &= ~0x02;
    }
}

void GtpUMessage::setPduNumberFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= 0x01;
    }
    else
    {
        fixedField_ &= ~0x01;
    }
}

void GtpUMessage::setProtocolType()
{
    fixedField_ |= 0x10;
}
