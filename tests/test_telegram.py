from nonebot import get_driver
from nonebot.adapters.telegram import Adapter, Bot
from nonebot.adapters.telegram.config import BotConfig
from nonebot.adapters.telegram.event import (
    ForumTopicMessageEvent,
    GroupMessageEvent,
    InlineEvent,
    PrivateMessageEvent,
)
from nonebug.app import App

from .utils import assert_session, assert_session_id


def new_bot(self_id: str) -> Bot:
    return Bot(adapter=Adapter(get_driver()), config=BotConfig(token=f"{self_id}:xxx"))


def test_private_message_event():
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot("2233")
    event = PrivateMessageEvent.parse_obj(
        {
            "message_id": 1234,
            "date": 1122,
            "chat": {"id": 3344, "type": "private"},
            "from": {
                "id": 3344,
                "first_name": "test",
                "is_bot": False,
            },
            "text": "123",
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Telegram",
        platform="telegram",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "telegram_Telegram_2233",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_3344",
        ),
    )


def test_group_message_event():
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot("2233")
    event = GroupMessageEvent.parse_obj(
        {
            "message_id": 1234,
            "date": 1122,
            "chat": {"id": 5566, "type": "group"},
            "from": {
                "id": 3344,
                "first_name": "test",
                "is_bot": False,
            },
            "text": "123",
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Telegram",
        platform="telegram",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="5566",
        id3=None,
    )
    assert_session_id(
        session,
        (
            "telegram_Telegram_2233",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_5566",
            "telegram_Telegram_2233_5566_3344",
            "telegram_Telegram_2233_5566",
            "telegram_Telegram_2233_5566_3344",
            "telegram_Telegram_2233_5566",
            "telegram_Telegram_2233_5566_3344",
        ),
    )


def test_forum_topic_message_event():
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot("2233")
    event = ForumTopicMessageEvent.parse_obj(
        {
            "message_id": 1234,
            "date": 1122,
            "chat": {"id": 5566, "type": "channel"},
            "from": {
                "id": 3344,
                "first_name": "test",
                "is_bot": False,
            },
            "message_thread_id": 6677,
            "text": "123",
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Telegram",
        platform="telegram",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="6677",
        id3="5566",
    )
    assert_session_id(
        session,
        (
            "telegram_Telegram_2233",
            "telegram_Telegram_2233_3344",
            "telegram_Telegram_2233_6677",
            "telegram_Telegram_2233_6677_3344",
            "telegram_Telegram_2233_5566",
            "telegram_Telegram_2233_5566_3344",
            "telegram_Telegram_2233_5566_6677",
            "telegram_Telegram_2233_5566_6677_3344",
        ),
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot("2233")
    event = InlineEvent()
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Telegram",
        platform="telegram",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
    assert_session_id(
        session,
        (
            "telegram_Telegram_2233",
            "telegram_Telegram_2233",
            "telegram_Telegram_2233",
            "telegram_Telegram_2233",
            "telegram_Telegram_2233",
            "telegram_Telegram_2233",
            "telegram_Telegram_2233",
            "telegram_Telegram_2233",
        ),
    )
