from cumplo_common.models.channel.channel import ChannelConfiguration, ChannelType
from cumplo_common.models.channel.ifttt import IFTTTConfiguration
from cumplo_common.models.channel.webhook import WebhookConfiguration
from cumplo_common.models.channel.whatsapp import WhatsappConfiguration

CHANNEL_CONFIGURATION_BY_TYPE = {
    ChannelType.WHATSAPP: WhatsappConfiguration,
    ChannelType.WEBHOOK: WebhookConfiguration,
    ChannelType.IFTTT: IFTTTConfiguration,
}
