from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.telegram import Bot, Event
    from nonebot.adapters.telegram.event import (
        ChannelPostEvent,
        EditedChannelPostEvent,
        ForumTopicEditedMessageEvent,
        ForumTopicMessageEvent,
        GroupEditedMessageEvent,
        GroupMessageEvent,
        LeftChatMemberEvent,
        NewChatMemberEvent,
        PrivateEditedMessageEvent,
        PrivateMessageEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.telegram

        def extract_level(self) -> SessionLevel:
            if isinstance(self.event, (PrivateMessageEvent, PrivateEditedMessageEvent)):
                return SessionLevel.LEVEL1

            elif isinstance(
                self.event,
                (
                    ForumTopicMessageEvent,
                    ChannelPostEvent,
                    ForumTopicEditedMessageEvent,
                    EditedChannelPostEvent,
                ),
            ):
                return SessionLevel.LEVEL3

            elif isinstance(
                self.event,
                (
                    GroupMessageEvent,
                    GroupEditedMessageEvent,
                    LeftChatMemberEvent,
                    NewChatMemberEvent,
                ),
            ):
                return SessionLevel.LEVEL2

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(
                self.event, (ForumTopicMessageEvent, ForumTopicEditedMessageEvent)
            ):
                return str(self.event.message_thread_id)

            elif isinstance(
                self.event,
                (
                    GroupMessageEvent,
                    GroupEditedMessageEvent,
                    LeftChatMemberEvent,
                    NewChatMemberEvent,
                ),
            ):
                return str(self.event.chat.id)

        def extract_id3(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    ForumTopicMessageEvent,
                    ChannelPostEvent,
                    ForumTopicEditedMessageEvent,
                    EditedChannelPostEvent,
                ),
            ):
                return str(self.event.chat.id)

except ImportError:
    pass
