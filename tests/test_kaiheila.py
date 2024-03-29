from nonebot import get_driver
from nonebot.adapters.kaiheila import Adapter, Bot, Message
from nonebot.adapters.kaiheila.event import (
    ChannelMessageEvent,
    EventMessage,
    Extra,
    PrivateMessageEvent,
    User,
)
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    return Bot(adapter=Adapter(get_driver()), self_id=self_id, name="test", token="")


def test_private_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = PrivateMessageEvent(
        post_type="message",
        channel_type="PERSON",
        type=1,
        target_id="6677",
        author_id="3344",
        content="123",
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(
            type=1,
            guild_id=None,
            channel_name=None,
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            author=None,
            body=None,
            attachments=None,
            code=None,
        ),
        user_id="3344",
        self_id="2233",
        message_type="private",
        sub_type="",
        event=EventMessage(
            type=1,
            guild_id=None,
            channel_name=None,
            content=Message("123"),
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            nav_channels=[],
            author=User(id="3344"),
            kmarkdown=None,
            attachments=None,
            code=None,
        ),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Kaiheila",
        platform="kaiheila",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2=None,
        id3=None,
    )


def test_channel_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = ChannelMessageEvent(
        post_type="message",
        channel_type="GROUP",
        type=1,
        target_id="6677",
        author_id="3344",
        content="123",
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(
            type=1,
            guild_id="5566",
            channel_name="test",
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            author=None,
            body=None,
            attachments=None,
            code=None,
        ),
        user_id="3344",
        self_id="2233",
        group_id="6677",
        message_type="group",
        sub_type="",
        event=EventMessage(
            type=1,
            guild_id="5566",
            channel_name="test",
            content=Message("123"),
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            nav_channels=[],
            author=User(id="3344"),
            kmarkdown=None,
            attachments=None,
            code=None,
        ),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Kaiheila",
        platform="kaiheila",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="6677",
        id3="5566",
    )


def test_server_message(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = ChannelMessageEvent(
        post_type="message",
        channel_type="GROUP",
        type=255,
        target_id="6677",
        author_id="3344",
        content="[系统消息]",
        msg_id="4455",
        msg_timestamp=1234,
        nonce="",
        extra=Extra(
            type=1,
            guild_id="5566",
            channel_name="test",
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            author=None,
            body=None,
            attachments=None,
            code=None,
        ),
        user_id="3344",
        self_id="2233",
        group_id="6677",
        message_type="group",
        sub_type="",
        event=EventMessage(
            type=1,
            guild_id="5566",
            channel_name="test",
            content=Message("[系统消息]"),
            mention=[],
            mention_all=False,
            mention_roles=[],
            mention_here=False,
            nav_channels=[],
            author=User(id="3344"),
            kmarkdown=None,
            attachments=None,
            code=None,
        ),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Kaiheila",
        platform="kaiheila",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2=None,
        id3="6677",
    )
