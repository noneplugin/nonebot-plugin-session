from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.console import Bot, Event

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.console

        def extract_level(self) -> SessionLevel:
            return SessionLevel.LEVEL1

        def extract_id1(self) -> str:
            return self.event.user.id

except ImportError:
    pass
