from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.villa import Bot, Event
    from nonebot.adapters.villa.event import (
        AddQuickEmoticonEvent,
        AuditCallbackEvent,
        ClickMsgComponentEvent,
        SendMessageEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.villa

        def extract_level(self) -> SessionLevel:
            return SessionLevel.LEVEL3

        def extract_id2(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    SendMessageEvent,
                    AddQuickEmoticonEvent,
                    AuditCallbackEvent,
                    ClickMsgComponentEvent,
                ),
            ):
                return str(self.event.room_id)

        def extract_id3(self) -> Optional[str]:
            return str(self.event.robot.villa_id)

except ImportError:
    pass
