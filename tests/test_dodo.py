from datetime import datetime

from nonebot import get_driver
from nonebot.adapters.dodo import Adapter, Bot
from nonebot.adapters.dodo.config import BotConfig
from nonebot.adapters.dodo.event import (
    ChannelMessageEvent,
    EventType,
    PersonalMessageEvent,
)
from nonebot.adapters.dodo.models import Member, MessageType, Personal, Sex, TextMessage
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    return Bot(
        adapter=Adapter(get_driver()),
        self_id=self_id,
        bot_config=BotConfig(client_id=self_id, token="qweasdzxc"),
    )


def test_private_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = PersonalMessageEvent(
        event_id="123",
        event_type=EventType.PERSONAL_MESSAGE,
        timestamp=datetime.now(),
        dodo_source_id="123",
        personal=Personal(nick_name="aa", avatar_url="qwe", sex=Sex.MALE),
        message_id="123",
        message_type=MessageType.TEXT,
        message_body=TextMessage(content="hello"),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="DoDo",
        platform="dodo",
        level=SessionLevel.LEVEL1,
        id1="123",
        id2=None,
        id3=None,
    )


def test_channel_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = ChannelMessageEvent(
        event_id="123",
        event_type=EventType.MESSAGE,
        timestamp=datetime.now(),
        dodo_source_id="123",
        island_source_id="789",
        channel_id="456",
        personal=Personal(nick_name="aa", avatar_url="qwe", sex=Sex.MALE),
        message_id="123",
        message_type=MessageType.TEXT,
        message_body=TextMessage(content="hello"),
        member=Member(nick_name="aa", join_time=datetime.now()),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="DoDo",
        platform="dodo",
        level=SessionLevel.LEVEL3,
        id1="123",
        id2="456",
        id3="789",
    )
