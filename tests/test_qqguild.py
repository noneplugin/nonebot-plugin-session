from nonebot import get_driver
from nonebot.adapters.qqguild import Adapter, Bot
from nonebot.adapters.qqguild.api import User
from nonebot.adapters.qqguild.config import BotInfo
from nonebot.adapters.qqguild.event import (
    DirectMessageCreateEvent,
    EventType,
    MessageCreateEvent,
    MetaEvent,
)
from nonebug.app import App

from .utils import assert_session, assert_session_id


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
        __type__=EventType.CHANNEL_CREATE,
        channel_id=6677,
        guild_id=5566,
        author=User(id=3344),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ Guild",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="6677",
        id3="5566",
    )
    assert_session_id(
        session,
        (
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233_3344",
            "qqguild_QQ Guild_2233_6677",
            "qqguild_QQ Guild_2233_6677_3344",
            "qqguild_QQ Guild_2233_5566",
            "qqguild_QQ Guild_2233_5566_3344",
            "qqguild_QQ Guild_2233_5566_6677",
            "qqguild_QQ Guild_2233_5566_6677_3344",
        ),
    )


def test_direct_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = DirectMessageCreateEvent(
        __type__=EventType.DIRECT_MESSAGE_CREATE,
        guild_id=5566,
        author=User(id=3344),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ Guild",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2=None,
        id3="5566",
    )
    assert_session_id(
        session,
        (
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233_3344",
            "qqguild_QQ Guild_2233_",
            "qqguild_QQ Guild_2233__3344",
            "qqguild_QQ Guild_2233_5566",
            "qqguild_QQ Guild_2233_5566_3344",
            "qqguild_QQ Guild_2233_5566_",
            "qqguild_QQ Guild_2233_5566__3344",
        ),
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = MetaEvent(__type__=EventType.READY)
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="QQ Guild",
        platform="qqguild",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233",
            "qqguild_QQ Guild_2233",
        ),
    )
