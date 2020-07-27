#ifndef GTPU_INTERFACES_IMESSAGE_H
#define GTPU_INTERFACES_IMESSAGE_H

#include <vector>

// IPC Message interface
class IMessage
{
public:
    enum MessageType
    {
        UnDefined        = 0,
        EchoRequest      = 1,
        EchoResponse     = 2,
        ErrorIndication  = 26,
        ExtensionHeaders = 31,
        EndMarker        = 254,
        GPDU             = 255,
    };

    virtual MessageType getMessageType() const = 0;

    virtual void serialize(std::vector<char>& data) = 0;

    virtual void unserialize(std::vector<char>& data) = 0;
};

#endif // GTPU_INTERFACES_IMESSAGE_H
