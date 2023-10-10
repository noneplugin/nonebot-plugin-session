from nonebot import get_driver
from nonebot.adapters.discord import (
    Adapter,
    Bot,
    DirectMessageCreateEvent,
    EventType,
    GuildMessageCreateEvent,
    HelloEvent,
)
from nonebot.adapters.discord.api.model import MessageFlag, MessageType, User
from nonebot.adapters.discord.config import BotInfo
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    return Bot(
        adapter=Adapter(get_driver()), self_id=self_id, bot_info=BotInfo(token="1234")
    )


def test_guild_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = GuildMessageCreateEvent.parse_obj(
        {
            "id": 1234,
            "channel_id": 5566,
            "guild_id": 6677,
            "author": User(
                **{
                    "id": 3344,
                    "username": "bot",
                    "discriminator": "0",
                    "avatar": None,
                }
            ),
            "content": "",
            "timestamp": 1,
            "edited_timestamp": None,
            "tts": False,
            "mention_everyone": False,
            "mentions": [],
            "mention_roles": [],
            "attachments": [],
            "embeds": [],
            "nonce": 3210,
            "pinned": False,
            "type": MessageType(0),
            "flags": MessageFlag(0),
            "referenced_message": None,
            "components": [],
            "to_me": False,
            "reply": None,
            "_message": [],
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Discord",
        platform="discord",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="5566",
        id3="6677",
    )


def test_direct_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = DirectMessageCreateEvent.parse_obj(
        {
            "id": 1234,
            "channel_id": 5566,
            "author": User(
                **{
                    "id": 3344,
                    "username": "bot",
                    "discriminator": "0",
                    "avatar": None,
                }
            ),
            "content": "",
            "timestamp": 1,
            "edited_timestamp": None,
            "tts": False,
            "mention_everyone": False,
            "mentions": [],
            "mention_roles": [],
            "attachments": [],
            "embeds": [],
            "nonce": 3210,
            "pinned": False,
            "type": MessageType(0),
            "flags": MessageFlag(0),
            "referenced_message": None,
            "components": [],
            "to_me": False,
            "reply": None,
            "_message": [],
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Discord",
        platform="discord",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2="5566",
        id3=None,
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = HelloEvent(__type__=EventType.HELLO, heartbeat_interval=10)
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Discord",
        platform="discord",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
