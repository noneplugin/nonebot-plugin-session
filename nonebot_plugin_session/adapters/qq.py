from typing import Optional

from ..const import SupportedPlatform
from ..extractor import SessionExtractor, register_session_extractor
from ..session import SessionLevel

try:
    from nonebot.adapters.qq import (
        AudioEvent,
        Bot,
        ChannelEvent,
        DirectMessageDeleteEvent,
        Event,
        EventType,
        ForumEvent,
        GroupAtMessageCreateEvent,
        GroupRobotEvent,
        GuildEvent,
        GuildMemberEvent,
        GuildMessageEvent,
        MessageAuditEvent,
        MessageDeleteEvent,
        MessageReactionEvent,
        PublicMessageDeleteEvent,
    )

    @register_session_extractor(Bot, Event)
    class EventExtractor(SessionExtractor[Bot, Event]):
        def extract_platform(self) -> str:
            if self.event.__type__ in [
                # C2C_GROUP_AT_MESSAGES
                EventType.C2C_MESSAGE_CREATE,
                EventType.GROUP_AT_MESSAGE_CREATE,
                # FRIEND_ROBOT_EVENT
                EventType.FRIEND_ADD,
                EventType.FRIEND_DEL,
                EventType.C2C_MSG_REJECT,
                EventType.C2C_MSG_RECEIVE,
                # GROUP_ROBOT_EVENT
                EventType.GROUP_ADD_ROBOT,
                EventType.GROUP_DEL_ROBOT,
                EventType.GROUP_MSG_REJECT,
                EventType.GROUP_MSG_RECEIVE,
            ]:
                return SupportedPlatform.qq

            elif self.event.__type__ in [
                # GUILDS
                EventType.GUILD_CREATE,
                EventType.GUILD_UPDATE,
                EventType.GUILD_DELETE,
                EventType.CHANNEL_CREATE,
                EventType.CHANNEL_UPDATE,
                EventType.CHANNEL_DELETE,
                # GUILD_MEMBERS
                EventType.GUILD_MEMBER_ADD,
                EventType.GUILD_MEMBER_UPDATE,
                EventType.GUILD_MEMBER_REMOVE,
                # GUILD_MESSAGES
                EventType.MESSAGE_CREATE,
                EventType.MESSAGE_DELETE,
                # GUILD_MESSAGE_REACTIONS
                EventType.MESSAGE_REACTION_ADD,
                EventType.MESSAGE_REACTION_REMOVE,
                # DIRECT_MESSAGE
                EventType.DIRECT_MESSAGE_CREATE,
                EventType.DIRECT_MESSAGE_DELETE,
                # OPEN_FORUMS_EVENT
                EventType.OPEN_FORUM_THREAD_CREATE,
                EventType.OPEN_FORUM_THREAD_UPDATE,
                EventType.OPEN_FORUM_THREAD_DELETE,
                EventType.OPEN_FORUM_POST_CREATE,
                EventType.OPEN_FORUM_POST_DELETE,
                EventType.OPEN_FORUM_REPLY_CREATE,
                EventType.OPEN_FORUM_REPLY_DELETE,
                # AUDIO_OR_LIVE_CHANNEL_MEMBER
                EventType.AUDIO_OR_LIVE_CHANNEL_MEMBER_ENTER,
                EventType.AUDIO_OR_LIVE_CHANNEL_MEMBER_EXIT,
                # INTERACTION
                EventType.INTERACTION_CREATE,
                # MESSAGE_AUDIT
                EventType.MESSAGE_AUDIT_PASS,
                EventType.MESSAGE_AUDIT_REJECT,
                # FORUM_EVENT
                EventType.FORUM_THREAD_CREATE,
                EventType.FORUM_THREAD_UPDATE,
                EventType.FORUM_THREAD_DELETE,
                EventType.FORUM_POST_CREATE,
                EventType.FORUM_POST_DELETE,
                EventType.FORUM_REPLY_CREATE,
                EventType.FORUM_REPLY_DELETE,
                EventType.FORUM_PUBLISH_AUDIT_RESULT,
                # AUDIO_ACTION
                EventType.AUDIO_START,
                EventType.AUDIO_FINISH,
                EventType.AUDIO_ON_MIC,
                EventType.AUDIO_OFF_MIC,
                # AT_MESSAGES
                EventType.AT_MESSAGE_CREATE,
                EventType.PUBLIC_MESSAGE_DELETE,
            ]:
                return SupportedPlatform.qqguild

            return SupportedPlatform.unknown

        def extract_level(self) -> SessionLevel:
            if self.event.__type__ in [
                EventType.C2C_MESSAGE_CREATE,
                # FRIEND_ROBOT_EVENT
                EventType.FRIEND_ADD,
                EventType.FRIEND_DEL,
                EventType.C2C_MSG_REJECT,
                EventType.C2C_MSG_RECEIVE,
            ]:
                return SessionLevel.LEVEL1

            elif self.event.__type__ in [
                # DIRECT_MESSAGE
                EventType.DIRECT_MESSAGE_CREATE,
                EventType.DIRECT_MESSAGE_DELETE,
            ]:
                return SessionLevel.LEVEL1

            elif self.event.__type__ in [
                EventType.GROUP_AT_MESSAGE_CREATE,
                # GROUP_ROBOT_EVENT
                EventType.GROUP_ADD_ROBOT,
                EventType.GROUP_DEL_ROBOT,
                EventType.GROUP_MSG_REJECT,
                EventType.GROUP_MSG_RECEIVE,
            ]:
                return SessionLevel.LEVEL2

            elif self.event.__type__ in [
                # GUILDS
                EventType.GUILD_CREATE,
                EventType.GUILD_UPDATE,
                EventType.GUILD_DELETE,
                EventType.CHANNEL_CREATE,
                EventType.CHANNEL_UPDATE,
                EventType.CHANNEL_DELETE,
                # GUILD_MEMBERS
                EventType.GUILD_MEMBER_ADD,
                EventType.GUILD_MEMBER_UPDATE,
                EventType.GUILD_MEMBER_REMOVE,
                # GUILD_MESSAGES
                EventType.MESSAGE_CREATE,
                EventType.MESSAGE_DELETE,
                # GUILD_MESSAGE_REACTIONS
                EventType.MESSAGE_REACTION_ADD,
                EventType.MESSAGE_REACTION_REMOVE,
                # OPEN_FORUMS_EVENT
                EventType.OPEN_FORUM_THREAD_CREATE,
                EventType.OPEN_FORUM_THREAD_UPDATE,
                EventType.OPEN_FORUM_THREAD_DELETE,
                EventType.OPEN_FORUM_POST_CREATE,
                EventType.OPEN_FORUM_POST_DELETE,
                EventType.OPEN_FORUM_REPLY_CREATE,
                EventType.OPEN_FORUM_REPLY_DELETE,
                # AUDIO_OR_LIVE_CHANNEL_MEMBER
                EventType.AUDIO_OR_LIVE_CHANNEL_MEMBER_ENTER,
                EventType.AUDIO_OR_LIVE_CHANNEL_MEMBER_EXIT,
                # INTERACTION
                EventType.INTERACTION_CREATE,
                # MESSAGE_AUDIT
                EventType.MESSAGE_AUDIT_PASS,
                EventType.MESSAGE_AUDIT_REJECT,
                # FORUM_EVENT
                EventType.FORUM_THREAD_CREATE,
                EventType.FORUM_THREAD_UPDATE,
                EventType.FORUM_THREAD_DELETE,
                EventType.FORUM_POST_CREATE,
                EventType.FORUM_POST_DELETE,
                EventType.FORUM_REPLY_CREATE,
                EventType.FORUM_REPLY_DELETE,
                EventType.FORUM_PUBLISH_AUDIT_RESULT,
                # AUDIO_ACTION
                EventType.AUDIO_START,
                EventType.AUDIO_FINISH,
                EventType.AUDIO_ON_MIC,
                EventType.AUDIO_OFF_MIC,
                # AT_MESSAGES
                EventType.AT_MESSAGE_CREATE,
                EventType.PUBLIC_MESSAGE_DELETE,
            ]:
                return SessionLevel.LEVEL3

            return SessionLevel.LEVEL0

        def extract_id2(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    GroupAtMessageCreateEvent,
                    GroupRobotEvent,
                ),
            ):
                return self.event.group_openid

            elif isinstance(
                self.event,
                (
                    GuildMessageEvent,
                    MessageReactionEvent,
                    MessageAuditEvent,
                    ForumEvent,
                    AudioEvent,
                ),
            ):
                return self.event.channel_id

            elif isinstance(
                self.event,
                (
                    MessageDeleteEvent,
                    DirectMessageDeleteEvent,
                    PublicMessageDeleteEvent,
                ),
            ):
                return self.event.message.channel_id

            elif isinstance(self.event, ChannelEvent):
                return self.event.id

        def extract_id3(self) -> Optional[str]:
            if isinstance(
                self.event,
                (
                    ChannelEvent,
                    GuildMemberEvent,
                    GuildMessageEvent,
                    MessageReactionEvent,
                    MessageAuditEvent,
                    ForumEvent,
                    AudioEvent,
                ),
            ):
                return self.event.guild_id

            elif isinstance(
                self.event,
                (
                    MessageDeleteEvent,
                    DirectMessageDeleteEvent,
                    PublicMessageDeleteEvent,
                ),
            ):
                return self.event.message.guild_id

            elif isinstance(self.event, GuildEvent):
                return self.event.id

except ImportError:
    pass
