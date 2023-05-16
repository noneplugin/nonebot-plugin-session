from datetime import datetime

from nonebot import get_driver
from nonebot.adapters.console import Adapter, Bot, Message, MessageEvent, User
from nonebug.app import App

from .utils import assert_session, assert_session_id


def new_bot(self_id: str) -> Bot:
    return Bot(adapter=Adapter(get_driver()), self_id=self_id)


def test_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = MessageEvent(
        time=datetime.now(),
        self_id="2233",
        post_type="message",
        user=User(id="3344"),
        message=Message("123"),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Console",
        platform="console",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "console_Console_2233",
            "console_Console_2233_3344",
            "console_Console_2233_3344",
            "console_Console_2233_3344",
            "console_Console_2233_3344",
            "console_Console_2233_3344",
            "console_Console_2233_3344",
            "console_Console_2233_3344",
        ),
    )
