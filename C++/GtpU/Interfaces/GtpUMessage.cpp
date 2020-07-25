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
    return static_cast<GtpUMessage::ProtocolType>((fixedField_ & ProtocolTypeFlag) >> 4);
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
        fixedField_ |= ExtentionFlag;
    }
    else
    {
        fixedField_ &= ~ExtentionFlag;
    }
}

void GtpUMessage::setSequenceFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= SequenceFlag;
    }
    else
    {
        fixedField_ &= ~SequenceFlag;
    }
}

void GtpUMessage::setPduNumberFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= PduNumberFlag;
    }
    else
    {
        fixedField_ &= ~PduNumberFlag;
    }
}

void GtpUMessage::setProtocolType()
{
    fixedField_ |= ProtocolTypeFlag;
}
