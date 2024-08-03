from typing import Optional

from nonebot import get_driver
from nonebot.adapters.satori import Adapter, Bot
from nonebot.adapters.satori.config import ClientInfo
from nonebot.adapters.satori.event import (
    InternalEvent,
    PrivateMessageCreatedEvent,
    PublicMessageCreatedEvent,
)
from nonebot.adapters.satori.models import Login, LoginStatus, User
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str, platform: str = "kook") -> Bot:
    return Bot(
        adapter=Adapter(get_driver()),
        self_id=self_id,
        login=Login(
            user=User(id=self_id),
            self_id=self_id,
            platform=platform,
            status=LoginStatus.ONLINE,
        ),
        info=ClientInfo(port=5140),
    )


def event_json(
    platform: str = "kook",
    self_id: str = "2233",
    user_id: str = "3344",
    channel_id: str = "6677",
    guild_id: Optional[str] = None,
) -> dict:
    return {
        "id": 5,
        "type": "message-created",
        "platform": platform,
        "self_id": self_id,
        "timestamp": 1700000000,
        "channel": {
            "id": channel_id,
            "type": 1,
            "name": "test",
        },
        "guild": {"id": guild_id, "name": "test"} if guild_id else None,
        "member": {
            "user": {
                "id": user_id,
                "name": "test",
            },
            "name": "test",
            "joined_at": 1700000000,
        },
        "message": {
            "id": "6b701984-c185-4da9-9808-549dc9947b85",
            "content": "text",
            "timestamp": 1700000001,
        },
        "user": {
            "id": user_id,
            "name": "test",
        },
    }


def test_private_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = PrivateMessageCreatedEvent.model_validate(
        event_json(),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="kaiheila",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2="6677",
        id3=None,
    )


def test_group_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233", platform="chronocat")
    event = PublicMessageCreatedEvent.model_validate(
        event_json(platform="chronocat"),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="6677",
        id3=None,
    )


def test_channel_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233", platform="qqguild")
    event = PublicMessageCreatedEvent.model_validate(
        event_json(platform="qqguild", guild_id="5566")
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="qqguild",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="6677",
        id3="5566",
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = InternalEvent.model_validate(
        {
            "id": 4,
            "type": "internal",
            "platform": "kook",
            "self_id": "2233",
            "timestamp": 17000000000,
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="kaiheila",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )


def test_unknown_platform(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233", platform="villa")
    event = InternalEvent.model_validate(
        {
            "id": 4,
            "type": "internal",
            "platform": "villa",
            "self_id": "2233",
            "timestamp": 17000000000,
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="unknown",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
