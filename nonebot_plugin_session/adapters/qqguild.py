from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.qqguild import (
        Bot,
        DirectMessageCreateEvent,
        Event,
        MessageAuditEvent,
        MessageEvent,
        MessageReactionEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.qqguild

        def extract_level(self) -> SessionLevel:
            if isinstance(self.event, DirectMessageCreateEvent):
                return SessionLevel.LEVEL1
            elif isinstance(
                self.event,
                (
                    MessageEvent,
                    MessageAuditEvent,
                    MessageReactionEvent,
                ),
            ):
                return SessionLevel.LEVEL3

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(
                self.event, (MessageEvent, MessageAuditEvent, MessageReactionEvent)
            ):
                if id := self.event.channel_id:
                    return str(id)

        def extract_id3(self) -> Optional[str]:
            if isinstance(
                self.event, (MessageEvent, MessageAuditEvent, MessageReactionEvent)
            ):
                if id := self.event.guild_id:
                    return str(id)

except ImportError:
    pass
