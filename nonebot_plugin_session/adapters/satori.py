from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.satori import Bot
    from nonebot.adapters.satori.event import (
        Event,
        PrivateMessageEvent,
        PublicMessageEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            platform = self.event.platform
            if platform in ("onebot", "red", "chronocat"):
                return SupportedPlatform.qq
            elif platform in ("kook",):
                return SupportedPlatform.kaiheila
            elif platform in list(SupportedPlatform):
                return platform
            return SupportedPlatform.unknown

        def extract_level(self) -> SessionLevel:
            if isinstance(self.event, PrivateMessageEvent):
                return SessionLevel.LEVEL1
            elif isinstance(self.event, PublicMessageEvent):
                if self.event.guild:
                    return SessionLevel.LEVEL3
                return SessionLevel.LEVEL2

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if self.event.channel:
                return self.event.channel.id

        def extract_id3(self) -> Optional[str]:
            if self.event.guild:
                return self.event.guild.id

except ImportError:
    pass
