#include "GtpUHeader.h"


std::uint8_t GtpUHeader::getVersionNumber() const
{
    return (fixedField_ & 0xE0) >> 4;
}

GtpUHeader::ProtocolType GtpUHeader::getProtocolType() const
{
    return static_cast<GtpUHeader::ProtocolType>((fixedField_ & ProtocolTypeFlag) >> 4);
}

GtpUHeader::GtpUHeader()
{

}

GtpUHeader::~GtpUHeader()
{

}

void GtpUHeader::setExtentionFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= ExtentionFlag;
    }
    else
    {
        fixedField_ &= ~ExtentionFlag;
    }
}

void GtpUHeader::setSequenceFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= SequenceFlag;
    }
    else
    {
        fixedField_ &= ~SequenceFlag;
    }
}

void GtpUHeader::setPduNumberFlag(bool enabled)
{
    if (enabled)
    {
        fixedField_ |= PduNumberFlag;
    }
    else
    {
        fixedField_ &= ~PduNumberFlag;
    }
}

void GtpUHeader::setProtocolType()
{
    fixedField_ |= ProtocolTypeFlag;
}
