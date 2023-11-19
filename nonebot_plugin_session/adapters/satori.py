from typing import Optional

from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.satori import Bot, MessageEvent
    from nonebot.adapters.satori.models import ChannelType

    @register_session_extractor(Bot, MessageEvent)
    class EventExtractor(SessionExtractor[Bot, MessageEvent]):
        def extract_platform(self) -> str:
            return self.event.platform

        def extract_level(self) -> SessionLevel:
            if self.event.channel.type == ChannelType.DIRECT:
                return SessionLevel.LEVEL1
            elif self.event.guild is not None:
                return SessionLevel.LEVEL3
            return SessionLevel.LEVEL2

        def extract_id2(self) -> Optional[str]:
            return self.event.channel.id

        def extract_id3(self) -> Optional[str]:
            if self.event.guild is not None:
                return self.event.guild.id

except ImportError:
    pass
