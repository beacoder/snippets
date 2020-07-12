#ifndef GTPU_INTERFACES_GTPUMESSAGE_H
#define GTPU_INTERFACES_GTPUMESSAGE_H

#include "IMessage.h"


class GtpUMessage : public IMessage
{
public:
    enum MessageType
    {
        UnDefined       = 0,
        EchoRequest     = 1,
        EchoResponse    = 2,
        ErrorIndication = 26,
        EndMarker       = 254,
        GPDU            = 255,
    };

    std::uint16_t getMessageType() const;

private:
    //-----------Begin IMessage-------------------
    virtual std::uint16_t getMessageId() const;
    //-----------End IMessage---------------------

private:
    std::uint16_t messageType_;
};

#endif // GTPU_INTERFACES_GTPUMESSAGE_H
