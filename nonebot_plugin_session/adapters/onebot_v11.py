from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.onebot.v11 import (
        Bot,
        Event,
        FriendAddNoticeEvent,
        FriendRecallNoticeEvent,
        FriendRequestEvent,
        GroupAdminNoticeEvent,
        GroupBanNoticeEvent,
        GroupDecreaseNoticeEvent,
        GroupIncreaseNoticeEvent,
        GroupMessageEvent,
        GroupRecallNoticeEvent,
        GroupRequestEvent,
        GroupUploadNoticeEvent,
        PokeNotifyEvent,
        PrivateMessageEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            return SupportedPlatform.qq

        def extract_level(self) -> SessionLevel:
            if isinstance(
                self.event,
                (
                    FriendAddNoticeEvent,
                    FriendRecallNoticeEvent,
                    FriendRequestEvent,
                    PrivateMessageEvent,
                ),
            ):
                return SessionLevel.LEVEL1

            if isinstance(
                self.event,
                (
                    GroupAdminNoticeEvent,
                    GroupBanNoticeEvent,
                    GroupDecreaseNoticeEvent,
                    GroupIncreaseNoticeEvent,
                    GroupMessageEvent,
                    GroupRecallNoticeEvent,
                    GroupRequestEvent,
                    GroupUploadNoticeEvent,
                ),
            ):
                return SessionLevel.LEVEL2

            if isinstance(self.event, PokeNotifyEvent):
                if self.event.group_id is None:
                    return SessionLevel.LEVEL1
                else:
                    return SessionLevel.LEVEL2

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    GroupAdminNoticeEvent,
                    GroupBanNoticeEvent,
                    GroupDecreaseNoticeEvent,
                    GroupIncreaseNoticeEvent,
                    GroupMessageEvent,
                    GroupRecallNoticeEvent,
                    GroupRequestEvent,
                    GroupUploadNoticeEvent,
                ),
            ):
                return str(self.event.group_id)

            if (
                isinstance(self.event, PokeNotifyEvent)
                and self.event.group_id is not None
            ):
                return str(self.event.group_id)

except ImportError:
    pass
