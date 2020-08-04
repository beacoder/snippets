#include "EchoRequest.h"

EchoRequest::EchoRequest()
{

}

IMessage::MessageType EchoRequest::getMessageType() const
{
    return static_cast<IMessage::MessageType>(IMessage::EchoRequest);
}

void EchoRequest:serialize(std::vector<char>& data)
{

}

void EchoRequest:unserialize(std::vector<char>& data)
{

}
