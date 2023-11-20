from typing import Optional

from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.satori import Bot, MessageEvent
    from nonebot.adapters.satori.event import (
        PrivateMessageCreatedEvent,
        PublicMessageCreatedEvent,
    )

    @register_session_extractor(Bot, MessageEvent)
    class EventExtractor(SessionExtractor[Bot, MessageEvent]):
        def extract_platform(self) -> str:
            return self.event.platform

        def extract_level(self) -> SessionLevel:
            if isinstance(self.event, PrivateMessageCreatedEvent):
                return SessionLevel.LEVEL1
            elif isinstance(self.event, PublicMessageCreatedEvent):
                if self.event.guild is None:
                    return SessionLevel.LEVEL2
                return SessionLevel.LEVEL3

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            return self.event.channel.id

        def extract_id3(self) -> Optional[str]:
            if self.event.guild is not None:
                return self.event.guild.id

except ImportError:
    pass
