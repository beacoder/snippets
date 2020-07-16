#ifndef GTPU_INTERFACES_IMESSAGE_H
#define GTPU_INTERFACES_IMESSAGE_H

#include <cinttypes>
#include <cstdio>

// IPC Message interface
class IMessage
{
public:
    enum MessageId
    {
        UnDefined = 0,
        GtpU      = 1,
    };

    virtual MessageId getMessageId() const = 0;
};

#endif // GTPU_INTERFACES_IMESSAGE_H
