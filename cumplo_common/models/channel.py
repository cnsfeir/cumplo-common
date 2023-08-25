from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ChannelType(StrEnum):
    TELEGRAM = "telegram"
    WEBHOOK = "webhook"
    MAILGUN = "mailgun"
    IFTTT = "ifttt"
    SLACK = "slack"


class ChannelConfiguration(BaseModel):
    type_: ChannelType = Field(..., exclude=True)


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
