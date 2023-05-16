from datetime import datetime

from nonebot import get_driver
from nonebot.adapters.onebot.v12 import (
    Adapter,
    Bot,
    ChannelMessageEvent,
    GroupMessageEvent,
    HeartbeatMetaEvent,
    Message,
    PrivateMessageEvent,
)
from nonebot.adapters.onebot.v12.event import BotSelf
from nonebug.app import App

from nonebot_plugin_session import SessionLevel, extract_session

from .utils import assert_session, assert_session_id


def new_bot(self_id: str, impl: str, platform: str) -> Bot:
    return Bot(
        adapter=Adapter(get_driver()), self_id=self_id, impl=impl, platform=platform
    )


def test_private_message_event(app: App):
    bot = new_bot(self_id="2233", impl="walle-q", platform="qq")
    event = PrivateMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="private",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qq", user_id="2233"),
        message=Message("123"),
        original_message=Message("123"),
        alt_message="123",
        user_id="3344",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="OneBot V12",
        platform="qq",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233_3344",
            "qq_OneBot V12_2233_3344",
            "qq_OneBot V12_2233_3344",
            "qq_OneBot V12_2233_3344",
            "qq_OneBot V12_2233_3344",
            "qq_OneBot V12_2233_3344",
            "qq_OneBot V12_2233_3344",
        ),
    )


def test_group_message_event(app: App):
    bot = new_bot(self_id="2233", impl="walle-q", platform="qq")
    event = GroupMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="group",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qq", user_id="2233"),
        message=Message("123"),
        original_message=Message("123"),
        alt_message="123",
        user_id="3344",
        group_id="1122",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="OneBot V12",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="1122",
        id3=None,
    )
    assert_session_id(
        session,
        (
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233_3344",
            "qq_OneBot V12_2233_1122",
            "qq_OneBot V12_2233_1122_3344",
            "qq_OneBot V12_2233_1122",
            "qq_OneBot V12_2233_1122_3344",
            "qq_OneBot V12_2233_1122",
            "qq_OneBot V12_2233_1122_3344",
        ),
    )


def test_channel_message_event(app: App):
    bot = new_bot(self_id="2233", impl="all4one", platform="qqguild")
    event = ChannelMessageEvent(
        id="1122",
        time=datetime.now(),
        type="message",
        detail_type="channel",
        sub_type="",
        message_id="4455",
        self=BotSelf(platform="qqguild", user_id="2233"),
        message=Message("123"),
        original_message=Message("123"),
        alt_message="123",
        user_id="3344",
        guild_id="5566",
        channel_id="6677",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="OneBot V12",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="6677",
        id3="5566",
    )
    assert_session_id(
        session,
        (
            "qqguild_OneBot V12_2233",
            "qqguild_OneBot V12_2233_3344",
            "qqguild_OneBot V12_2233_6677",
            "qqguild_OneBot V12_2233_6677_3344",
            "qqguild_OneBot V12_2233_5566",
            "qqguild_OneBot V12_2233_5566_3344",
            "qqguild_OneBot V12_2233_5566_6677",
            "qqguild_OneBot V12_2233_5566_6677_3344",
        ),
    )


def test_undefined_event(app: App):
    bot = new_bot(self_id="2233", impl="walle-q", platform="qq")
    event = HeartbeatMetaEvent(
        id="1122",
        time=datetime.now(),
        type="meta",
        detail_type="heartbeat",
        sub_type="",
        interval=10,
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="OneBot V12",
        platform="qq",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233",
            "qq_OneBot V12_2233",
        ),
    )
