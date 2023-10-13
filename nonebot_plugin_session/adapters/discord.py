from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.discord import (
        Bot,
        DirectMessageCreateEvent,
        DirectMessageDeleteBulkEvent,
        DirectMessageDeleteEvent,
        DirectMessageReactionAddEvent,
        DirectMessageReactionRemoveAllEvent,
        DirectMessageReactionRemoveEmojiEvent,
        DirectMessageReactionRemoveEvent,
        DirectMessageUpdateEvent,
        DirectTypingStartEvent,
        Event,
        GuildMessageCreateEvent,
        GuildMessageDeleteBulkEvent,
        GuildMessageDeleteEvent,
        GuildMessageReactionAddEvent,
        GuildMessageReactionRemoveAllEvent,
        GuildMessageReactionRemoveEmojiEvent,
        GuildMessageReactionRemoveEvent,
        GuildMessageUpdateEvent,
        GuildTypingStartEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.discord

        def extract_level(self) -> SessionLevel:
            if isinstance(
                self.event,
                (
                    DirectMessageCreateEvent,
                    DirectMessageDeleteBulkEvent,
                    DirectMessageDeleteEvent,
                    DirectMessageUpdateEvent,
                    DirectMessageReactionAddEvent,
                    DirectMessageReactionRemoveAllEvent,
                    DirectMessageReactionRemoveEvent,
                    DirectMessageReactionRemoveEmojiEvent,
                    DirectTypingStartEvent,
                ),
            ):
                return SessionLevel.LEVEL1

            elif isinstance(
                self.event,
                (
                    GuildMessageCreateEvent,
                    GuildMessageDeleteBulkEvent,
                    GuildMessageDeleteEvent,
                    GuildMessageReactionAddEvent,
                    GuildMessageReactionRemoveAllEvent,
                    GuildMessageReactionRemoveEmojiEvent,
                    GuildMessageReactionRemoveEvent,
                    GuildMessageUpdateEvent,
                    GuildTypingStartEvent,
                ),
            ):
                return SessionLevel.LEVEL3

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    GuildMessageCreateEvent,
                    GuildMessageDeleteBulkEvent,
                    GuildMessageDeleteEvent,
                    GuildMessageReactionAddEvent,
                    GuildMessageReactionRemoveAllEvent,
                    GuildMessageReactionRemoveEmojiEvent,
                    GuildMessageReactionRemoveEvent,
                    GuildMessageUpdateEvent,
                    GuildTypingStartEvent,
                    DirectMessageCreateEvent,
                    DirectMessageDeleteBulkEvent,
                    DirectMessageDeleteEvent,
                    DirectMessageUpdateEvent,
                    DirectMessageReactionAddEvent,
                    DirectMessageReactionRemoveAllEvent,
                    DirectMessageReactionRemoveEvent,
                    DirectMessageReactionRemoveEmojiEvent,
                    DirectTypingStartEvent,
                ),
            ):
                return str(self.event.channel_id)

        def extract_id3(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    GuildMessageCreateEvent,
                    GuildMessageDeleteBulkEvent,
                    GuildMessageDeleteEvent,
                    GuildMessageReactionAddEvent,
                    GuildMessageReactionRemoveAllEvent,
                    GuildMessageReactionRemoveEmojiEvent,
                    GuildMessageReactionRemoveEvent,
                    GuildMessageUpdateEvent,
                    GuildTypingStartEvent,
                ),
            ):
                return str(self.event.guild_id)

except ImportError:
    pass
