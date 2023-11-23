from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.dodo import Bot, Event
    from nonebot.adapters.dodo.event import PersonalMessageEvent

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.dodo

        def extract_level(self) -> SessionLevel:
            if isinstance(self.event, PersonalMessageEvent):
                return SessionLevel.LEVEL1
            return SessionLevel.LEVEL3

        def extract_id2(self) -> Optional[str]:
            return getattr(self.event, "channel_id", None)

        def extract_id3(self) -> Optional[str]:
            return getattr(self.event, "island_source_id", None)

except ImportError:
    pass
