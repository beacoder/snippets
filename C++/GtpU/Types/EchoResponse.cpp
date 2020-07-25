#include "EchoResponse.h"

EchoResponse::EchoResponse()
{

}

IMessage::MessageType EchoResponse::getMessageType() const
{
    return static_cast<IMessage::MessageType>(IMessage::EchoResponse);
}

void EchoResponse:serialize(std::vector<char>& data)
{

}

void EchoResponse:unserialize(std::vector<char>& data)
{

}
