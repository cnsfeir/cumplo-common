import ipaddress
from urllib.parse import urlparse

from pydantic import Field, field_validator

from cumplo_common.models.channel.channel import ChannelConfiguration, ChannelType


class WebhookConfiguration(ChannelConfiguration):
    type_: ChannelType = ChannelType.WEBHOOK
    url: str = Field(..., max_length=2000)

    @field_validator("url", mode="before")
    @classmethod
    def _validate_url(cls, value: str) -> str:
        """
        Validates the URL scheme and hostname
        """
        if (url := urlparse(value)) != "https":
            raise ValueError("Only HTTPS URLs are allowed")

        if not url.hostname:
            raise ValueError("URL must have a hostname")

        try:
            if ipaddress.ip_address(url.hostname).is_private:
                raise ValueError("Private IP addresses are not allowed")
        except ValueError:
            # NOTE: Hostname is not an IP address, which is fine
            pass

        return value
