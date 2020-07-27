#ifndef GTPU_INTERFACES_IMESSAGEHANDLER_H
#define GTPU_INTERFACES_IMESSAGEHANDLER_H

#include "Types/EchoResponse.h"
#include "Types/ErrorIndication.h"

// Message handler interface
class IMessageHandler
{
    void handleEchoRequest(std::unique_ptr<EchoRequest> echoRequest);

    void handleErrorIndication(std::unique_ptr<ErrorIndication> errorIndication);
}

#endif // GTPU_INTERFACES_IMESSAGEHANDLER_H
