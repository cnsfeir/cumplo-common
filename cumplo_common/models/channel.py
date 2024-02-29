from pydantic import Field

from cumplo_common.models.base_model import BaseModel, StrEnum


class ChannelType(StrEnum):
    WEBHOOK = "WEBHOOK"
    IFTTT = "IFTTT"


class ChannelConfiguration(BaseModel):
    type_: ChannelType = Field(...)
    enabled: bool = Field(True)


class WebhookConfiguration(ChannelConfiguration):
    url: str = Field(...)
    type_: ChannelType = ChannelType.WEBHOOK


class IFTTTConfiguration(ChannelConfiguration):
    key: str = Field(...)
    event: str = Field(...)
    type_: ChannelType = ChannelType.IFTTT


CHANNEL_CONFIGURATION_BY_TYPE: dict[ChannelType, type[ChannelConfiguration]] = {
    ChannelType.WEBHOOK: WebhookConfiguration,
    ChannelType.IFTTT: IFTTTConfiguration,
}
