#include "GtpUMessage.h"

std::uint16_t GtpUMessage::getMessageId() const
{
    return GtpU;
}

std::uint16_t GtpUMessage::getMessageType() const
{
    return messageType_;
}
