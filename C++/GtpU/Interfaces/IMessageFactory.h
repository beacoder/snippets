#ifndef GTPU_INTERFACES_IMESSAGEFACTORY_H
#define GTPU_INTERFACES_IMESSAGEFACTORY_H

#include "Types/EchoResponse.h"
#include <memory>

class IMessageFactory
{
    virtual std::unique_ptr<EchoResponse> createEchoResponse() = 0;
}

#endif // GTPU_INTERFACES_IMESSAGEFACTORY_H
