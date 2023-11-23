from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.qq import (
        AtMessageCreateEvent,
        Bot,
        C2CMessageCreateEvent,
        DirectMessageCreateEvent,
        Event,
        GroupAtMessageCreateEvent,
        MessageAuditEvent,
        MessageCreateEvent,
        MessageReactionEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            if isinstance(
                self.event, (GroupAtMessageCreateEvent, C2CMessageCreateEvent)
            ):
                return SupportedPlatform.qq
            elif isinstance(
                self.event,
                (
                    MessageAuditEvent,
                    MessageReactionEvent,
                    MessageCreateEvent,
                    AtMessageCreateEvent,
                    DirectMessageCreateEvent,
                ),
            ):
                return SupportedPlatform.qqguild

            return SupportedPlatform.unknown

        def extract_level(self) -> SessionLevel:
            if isinstance(
                self.event, (DirectMessageCreateEvent, C2CMessageCreateEvent)
            ):
                return SessionLevel.LEVEL1
            elif isinstance(self.event, GroupAtMessageCreateEvent):
                return SessionLevel.LEVEL2
            elif isinstance(
                self.event,
                (
                    MessageAuditEvent,
                    MessageReactionEvent,
                    MessageCreateEvent,
                    AtMessageCreateEvent,
                ),
            ):
                return SessionLevel.LEVEL3

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(self.event, GroupAtMessageCreateEvent):
                return self.event.group_openid
            elif isinstance(
                self.event,
                (
                    MessageAuditEvent,
                    MessageReactionEvent,
                    MessageCreateEvent,
                    AtMessageCreateEvent,
                    DirectMessageCreateEvent,
                ),
            ):
                return self.event.channel_id

        def extract_id3(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    MessageAuditEvent,
                    MessageReactionEvent,
                    MessageCreateEvent,
                    AtMessageCreateEvent,
                    DirectMessageCreateEvent,
                ),
            ):
                return self.event.guild_id

except ImportError:
    pass
