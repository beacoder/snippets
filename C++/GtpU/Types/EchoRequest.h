#ifndef GTPU_TYPES_ECHOREQUEST_H
#define GTPU_TYPES_ECHOREQUEST_H

#include "GtpuHeader.h"


class EchoRequest : public IMessage
{
public:
    EchoRequest();

private:
    //-----------Begin IMessage-------------------
    IMessage::MessageType getMessageType() const override;
    void serialize(std::vector<char>& data) override;
    void unserialize(std::vector<char>& data) override;
    //-----------End IMessage---------------------

private:
    GtpuHeader header_;
};

#endif // GTPU_TYPES_ECHOREQUEST_H
