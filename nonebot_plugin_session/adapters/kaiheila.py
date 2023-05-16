from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.kaiheila import Bot, Event

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.kaiheila

        def extract_level(self) -> SessionLevel:
            if self.event.channel_type == "PERSON":
                return SessionLevel.LEVEL1
            elif self.event.channel_type == "GROUP":
                return SessionLevel.LEVEL3

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if self.event.channel_type == "GROUP":
                if self.event.type_ != 255:
                    return self.event.target_id

        def extract_id3(self) -> Optional[str]:
            if self.event.channel_type == "GROUP":
                if self.event.type_ == 255:
                    return self.event.target_id
                else:
                    return self.event.extra.guild_id

except ImportError:
    pass
