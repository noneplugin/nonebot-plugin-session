from nonebot import get_driver
from nonebot.adapters.onebot.v11 import (
    Adapter,
    Bot,
    GroupMessageEvent,
    HeartbeatMetaEvent,
    Message,
    PrivateMessageEvent,
)
from nonebot.adapters.onebot.v11.event import Sender, Status
from nonebug.app import App

from .utils import assert_session, assert_session_id


def new_bot(self_id: str) -> Bot:
    return Bot(adapter=Adapter(get_driver()), self_id=self_id)


def test_private_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = PrivateMessageEvent(
        time=1122,
        self_id=2233,
        post_type="message",
        sub_type="",
        user_id=3344,
        message_id=4455,
        message=Message("123"),
        original_message=Message("123"),
        message_type="private",
        raw_message="123",
        font=1,
        sender=Sender(user_id=3344),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_3344",
        ),
    )


def test_group_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = GroupMessageEvent(
        group_id=1122,
        time=1122,
        self_id=2233,
        post_type="message",
        sub_type="",
        user_id=3344,
        message_id=4455,
        message=Message("123"),
        original_message=Message("123"),
        message_type="group",
        raw_message="123",
        font=1,
        sender=Sender(user_id=3344),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="1122",
        id3=None,
    )
    assert_session_id(
        session,
        (
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_1122",
            "qq_OneBot V11_2233_1122_3344",
            "qq_OneBot V11_2233_1122",
            "qq_OneBot V11_2233_1122_3344",
            "qq_OneBot V11_2233_1122",
            "qq_OneBot V11_2233_1122_3344",
        ),
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = HeartbeatMetaEvent(
        time=1122,
        self_id=2233,
        post_type="meta_event",
        meta_event_type="heartbeat",
        status=Status(online=True, good=True),
        interval=10,
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233",
        ),
    )
