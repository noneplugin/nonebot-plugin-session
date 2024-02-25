from datetime import datetime

from nonebot import get_driver
from nonebot.adapters.qq import Adapter, Bot
from nonebot.adapters.qq.config import BotInfo
from nonebot.adapters.qq.event import (
    C2CMessageCreateEvent,
    ChannelCreateEvent,
    DirectMessageCreateEvent,
    EventType,
    GroupAtMessageCreateEvent,
    GuildDeleteEvent,
    MessageCreateEvent,
    MessageDeleteEvent,
    MetaEvent,
)
from nonebot.adapters.qq.models import (
    ChannelSubType,
    ChannelType,
    FriendAuthor,
    GroupMemberAuthor,
)
from nonebot.adapters.qq.models import Message as GuildMessage
from nonebot.adapters.qq.models import User
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    return Bot(
        adapter=Adapter(get_driver()),
        self_id=self_id,
        bot_info=BotInfo(id="", token="", secret=""),
    )


def test_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = MessageCreateEvent(
        id="123",
        __type__=EventType.CHANNEL_CREATE,
        channel_id="6677",
        guild_id="5566",
        author=User(id="3344"),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="6677",
        id3="5566",
    )


def test_direct_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = DirectMessageCreateEvent(
        id="id",
        __type__=EventType.DIRECT_MESSAGE_CREATE,
        channel_id="6677",
        guild_id="5566",
        author=User(id="3344"),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="qqguild",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2="6677",
        id3="5566",
    )


def test_c2c_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = C2CMessageCreateEvent(
        id="id",
        __type__=EventType.C2C_MESSAGE_CREATE,
        content="test",
        timestamp="2023-01-01T00:00:00",
        author=FriendAuthor(id="1111", user_openid="3344"),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="qq",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2=None,
        id3=None,
    )


def test_group_at_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = GroupAtMessageCreateEvent(
        id="id",
        __type__=EventType.C2C_MESSAGE_CREATE,
        content="test",
        timestamp="2023-01-01T00:00:00",
        author=GroupMemberAuthor(id="1111", member_openid="3344"),
        group_openid="6677",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="6677",
        id3=None,
    )


def test_message_delete_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = MessageDeleteEvent(
        __type__=EventType.MESSAGE_DELETE,
        message=GuildMessage(
            id="123",
            channel_id="6677",
            guild_id="5566",
            content="test",
            author=User(id="3344"),
        ),
        op_user=User(id="3344"),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1=None,
        id2="6677",
        id3="5566",
    )


def test_guild_delete_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = GuildDeleteEvent(
        __type__=EventType.GUILD_DELETE,
        id="5566",
        name="test",
        icon="icon",
        owner_id="3344",
        owner=True,
        member_count=1,
        max_members=100,
        description="description",
        joined_at=datetime.now(),
        op_user_id="3344",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1=None,
        id2=None,
        id3="5566",
    )


def test_channel_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = ChannelCreateEvent(
        __type__=EventType.CHANNEL_CREATE,
        id="6677",
        guild_id="5566",
        name="test",
        type=ChannelType.TEXT,
        sub_type=ChannelSubType.TALK,
        position=1,
        op_user_id="3344",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1=None,
        id2="6677",
        id3="5566",
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = MetaEvent(__type__=EventType.READY)
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ",
        platform="unknown",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
