#ifndef GTPU_TYPES_GTPUHEADER_H
#define GTPU_TYPES_GTPUHEADER_H

#include <cstdint>


class GtpUHeader
{
public:
    enum ProtocolType
    {
        GTP_Prime = 0,
        GTP       = 1,
    };

    enum HeaderFlag
    {
        PduNumberFlag    = 0x01,
        SequenceFlag     = 0x02,
        ExtentionFlag    = 0x04,
        ProtocolTypeFlag = 0x10,
    };

    GtpUHeader();
    ~GtpUHeader();

    std::uint8_t  getVersionNumber() const;
    ProtocolType  getProtocolType() const;

private:
    void setExtentionFlag(bool enabled);
    void setSequenceFlag(bool enabled);
    void setPduNumberFlag(bool enabled);
    void setProtocolType();

private:
    std::uint8_t  fixedField_;
    std::uint16_t messageType_;
};

#endif // GTPU_TYPES_GTPUHEADER_H
