from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.red import Bot
    from nonebot.adapters.red.api.model import ChatType
    from nonebot.adapters.red.event import (
        Event,
        GroupMessageEvent,
        NoticeEvent,
        PrivateMessageEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.qq

        def extract_level(self) -> SessionLevel:
            if isinstance(self.event, PrivateMessageEvent):
                return SessionLevel.LEVEL1

            elif isinstance(self.event, GroupMessageEvent):
                return SessionLevel.LEVEL2

            elif isinstance(self.event, NoticeEvent):
                if self.event.chatType == ChatType.FRIEND:
                    return SessionLevel.LEVEL1
                elif self.event.chatType == ChatType.GROUP:
                    return SessionLevel.LEVEL2

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(self.event, GroupMessageEvent) or (
                isinstance(self.event, NoticeEvent)
                and self.event.chatType == ChatType.GROUP
            ):
                return self.event.peerUin or self.event.peerUid

except ImportError:
    pass
