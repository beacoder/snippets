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

    enum ProtocolType
    {
        GTP_Prime = 0,
        GTP       = 1,
    };

    GtpUMessage();
    ~GtpUMessage();

    std::uint16_t getMessageType() const;
    std::uint8_t  getVersionNumber() const;
    ProtocolType  getProtocolType() const;

private:
    //-----------Begin IMessage-------------------
    virtual MessageId getMessageId() const;
    //-----------End IMessage---------------------

    void setExtentionFlag(bool enabled);
    void setSequenceFlag(bool enabled);
    void setPduNumberFlag(bool enabled);
    void setProtocolType();

private:
    std::uint8_t  fixedField_;
    std::uint16_t messageType_;
};

#endif // GTPU_INTERFACES_GTPUMESSAGE_H
