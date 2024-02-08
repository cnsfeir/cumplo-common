from typing import Any

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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(type_=ChannelType.WEBHOOK, *args, **kwargs)


class IFTTTConfiguration(ChannelConfiguration):
    key: str = Field(...)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(type_=ChannelType.IFTTT, *args, **kwargs)


CHANNEL_CONFIGURATION_BY_TYPE: dict[ChannelType, type[ChannelConfiguration]] = {
    ChannelType.WEBHOOK: WebhookConfiguration,
    ChannelType.IFTTT: IFTTTConfiguration,
}
