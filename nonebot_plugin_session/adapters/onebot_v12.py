from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.onebot.v12 import (
        Bot,
        ChannelCreateEvent,
        ChannelDeleteEvent,
        ChannelMemberDecreaseEvent,
        ChannelMemberIncreaseEvent,
        ChannelMessageDeleteEvent,
        ChannelMessageEvent,
        Event,
        FriendDecreaseEvent,
        FriendIncreaseEvent,
        GroupMemberDecreaseEvent,
        GroupMemberIncreaseEvent,
        GroupMessageDeleteEvent,
        GroupMessageEvent,
        GuildMemberDecreaseEvent,
        GuildMemberIncreaseEvent,
        PrivateMessageDeleteEvent,
        PrivateMessageEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            platform = self.bot.platform
            if platform in ("kook",):
                return SupportedPlatform.kaiheila
            elif platform in list(SupportedPlatform):
                return platform
            return SupportedPlatform.unknown

        def extract_level(self) -> SessionLevel:
            if isinstance(
                self.event,
                (
                    PrivateMessageDeleteEvent,
                    PrivateMessageEvent,
                    FriendDecreaseEvent,
                    FriendIncreaseEvent,
                ),
            ):
                return SessionLevel.LEVEL1

            elif isinstance(
                self.event,
                (
                    GroupMemberDecreaseEvent,
                    GroupMemberIncreaseEvent,
                    GroupMessageDeleteEvent,
                    GroupMessageEvent,
                ),
            ):
                return SessionLevel.LEVEL2

            elif isinstance(
                self.event,
                (
                    ChannelCreateEvent,
                    ChannelDeleteEvent,
                    ChannelMemberDecreaseEvent,
                    ChannelMemberIncreaseEvent,
                    ChannelMessageDeleteEvent,
                    ChannelMessageEvent,
                    GuildMemberDecreaseEvent,
                    GuildMemberIncreaseEvent,
                ),
            ):
                return SessionLevel.LEVEL3

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    GroupMemberDecreaseEvent,
                    GroupMemberIncreaseEvent,
                    GroupMessageDeleteEvent,
                    GroupMessageEvent,
                ),
            ):
                return self.event.group_id

            elif isinstance(
                self.event,
                (
                    ChannelCreateEvent,
                    ChannelDeleteEvent,
                    ChannelMemberDecreaseEvent,
                    ChannelMemberIncreaseEvent,
                    ChannelMessageDeleteEvent,
                    ChannelMessageEvent,
                ),
            ):
                return self.event.channel_id

        def extract_id3(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    ChannelCreateEvent,
                    ChannelDeleteEvent,
                    ChannelMemberDecreaseEvent,
                    ChannelMemberIncreaseEvent,
                    ChannelMessageDeleteEvent,
                    ChannelMessageEvent,
                    GuildMemberDecreaseEvent,
                    GuildMemberIncreaseEvent,
                ),
            ):
                return self.event.guild_id

except ImportError:
    pass
