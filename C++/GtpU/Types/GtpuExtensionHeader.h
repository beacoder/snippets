#ifndef GTPU_TYPES_GTPUEXTENSIONHEADER_H
#define GTPU_TYPES_GTPUEXTENSIONHEADER_H

#include "Types.h"

template<class Content>
class GtpuExtensionHeader
{
public:
    GtpuExtensionHeader();
    ~GtpuExtensionHeader();

private:
    std::uint8_t length_;
    Content      content_;
    std::uint8_t extensionType_;
};

using UdpPortHeader               = GtpuExtensionHeader<UdpPort>;
using PdcpPduNumberHeader         = GtpuExtensionHeader<PdcpPduNumber>;
using LongPdcpPduNumberHeader     = GtpuExtensionHeader<LongPdcpPduNumber>;
using ServiceClassIndicatorHeader = GtpuExtensionHeader<ServiceClassIndicator>;
using RanContainerHeader          = GtpuExtensionHeader<RanContainer>;
using XwRanContainerHeader        = GtpuExtensionHeader<XwRanContainer>;
using NrRanContainerHeader        = GtpuExtensionHeader<NrRanContainer>;
using PduSessionContainerHeader   = GtpuExtensionHeader<PduSessionContainer>;

#endif // GTPU_TYPES_GTPUEXTENSIONHEADER_H
