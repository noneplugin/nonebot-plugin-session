from nonebot import get_driver
from nonebot.adapters.satori import Adapter, Bot
from nonebot.adapters.satori.config import ClientInfo
from nonebot.adapters.satori.event import (
    InternalEvent,
    PrivateMessageCreatedEvent,
    PublicMessageCreatedEvent,
)
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    return Bot(
        adapter=Adapter(get_driver()),
        self_id=self_id,
        platform="kook",
        info=ClientInfo(port=5140),
    )


def test_private_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = PrivateMessageCreatedEvent.parse_obj(
        {
            "id": 5,
            "type": "message-created",
            "platform": "kook",
            "self_id": "2233",
            "timestamp": 1700000000,
            "argv": None,
            "button": None,
            "channel": {
                "id": "6677",
                "type": 1,
                "name": None,
                "parent_id": None,
            },
            "guild": None,
            "login": None,
            "member": {
                "user": None,
                "name": None,
                "nick": "Aislinn",
                "avatar": None,
                "joined_at": None,
            },
            "message": {
                "id": "6b701984-c185-4da9-9808-549dc9947b85",
                "content": [
                    {
                        "type": "text",
                        "attrs": {"text": "test"},
                        "children": [],
                        "source": None,
                    }
                ],
                "channel": None,
                "guild": None,
                "member": {
                    "user": {
                        "id": "3344",
                        "name": "Aislinn",
                        "nick": None,
                        "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                        "is_bot": None,
                        "discriminator": "4261",
                        "username": "Aislinn",
                        "user_id": "3344",
                    },
                    "name": None,
                    "nick": "Aislinn",
                    "avatar": None,
                    "joined_at": None,
                },
                "user": {
                    "id": "3344",
                    "name": "Aislinn",
                    "nick": None,
                    "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                    "is_bot": None,
                    "discriminator": "4261",
                    "username": "Aislinn",
                    "user_id": "3344",
                },
                "created_at": None,
                "updated_at": None,
                "elements": [
                    {"type": "text", "attrs": {"content": "test"}, "children": []}
                ],
                "timestamp": 1700475245789,
                "message_id": "6b701984-c185-4da9-9808-549dc9947b85",
            },
            "operator": None,
            "role": None,
            "user": {
                "id": "3344",
                "name": "Aislinn",
                "nick": None,
                "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                "is_bot": None,
                "discriminator": "4261",
                "username": "Aislinn",
                "user_id": "3344",
            },
            "_type": "kook",
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="kook",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2="6677",
        id3=None,
    )


def test_group_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = PublicMessageCreatedEvent.parse_obj(
        {
            "id": 4,
            "type": "message-created",
            "platform": "kook",
            "self_id": "2233",
            "timestamp": 17000000000,
            "argv": None,
            "button": None,
            "channel": {
                "id": "6677",
                "type": 0,
                "name": "文字频道",
                "parent_id": None,
            },
            "guild": None,
            "login": None,
            "member": {
                "user": None,
                "name": None,
                "nick": "Aislinn",
                "avatar": None,
                "joined_at": None,
            },
            "message": {
                "id": "56163f81-de30-4c39-b4c4-3a205d0be9da",
                "content": [
                    {
                        "type": "text",
                        "attrs": {"text": "test"},
                        "children": [],
                        "source": None,
                    }
                ],
                "channel": None,
                "guild": None,
                "member": {
                    "user": {
                        "id": "3344",
                        "name": "Aislinn",
                        "nick": None,
                        "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                        "is_bot": None,
                        "username": "Aislinn",
                        "user_id": "3344",
                        "discriminator": "4261",
                    },
                    "name": None,
                    "nick": "Aislinn",
                    "avatar": None,
                    "joined_at": None,
                },
                "user": {
                    "id": "3344",
                    "name": "Aislinn",
                    "nick": None,
                    "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                    "is_bot": None,
                    "username": "Aislinn",
                    "user_id": "3344",
                    "discriminator": "4261",
                },
                "created_at": None,
                "updated_at": None,
                "message_id": "56163f81-de30-4c39-b4c4-3a205d0be9da",
                "elements": [
                    {"type": "text", "attrs": {"content": "test"}, "children": []}
                ],
                "timestamp": 1700474858446,
            },
            "operator": None,
            "role": None,
            "user": {
                "id": "3344",
                "name": "Aislinn",
                "nick": None,
                "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                "is_bot": None,
                "username": "Aislinn",
                "user_id": "3344",
                "discriminator": "4261",
            },
            "_type": "kook",
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="kook",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="6677",
        id3=None,
    )


def test_channel_message_create_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = PublicMessageCreatedEvent.parse_obj(
        {
            "id": 4,
            "type": "message-created",
            "platform": "kook",
            "self_id": "2233",
            "timestamp": 17000000000,
            "argv": None,
            "button": None,
            "channel": {
                "id": "6677",
                "type": 0,
                "name": "文字频道",
                "parent_id": None,
            },
            "guild": {"id": "5566", "name": None, "avatar": None},
            "login": None,
            "member": {
                "user": None,
                "name": None,
                "nick": "Aislinn",
                "avatar": None,
                "joined_at": None,
            },
            "message": {
                "id": "56163f81-de30-4c39-b4c4-3a205d0be9da",
                "content": [
                    {
                        "type": "text",
                        "attrs": {"text": "test"},
                        "children": [],
                        "source": None,
                    }
                ],
                "channel": None,
                "guild": None,
                "member": {
                    "user": {
                        "id": "3344",
                        "name": "Aislinn",
                        "nick": None,
                        "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                        "is_bot": None,
                        "username": "Aislinn",
                        "user_id": "3344",
                        "discriminator": "4261",
                    },
                    "name": None,
                    "nick": "Aislinn",
                    "avatar": None,
                    "joined_at": None,
                },
                "user": {
                    "id": "3344",
                    "name": "Aislinn",
                    "nick": None,
                    "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                    "is_bot": None,
                    "username": "Aislinn",
                    "user_id": "3344",
                    "discriminator": "4261",
                },
                "created_at": None,
                "updated_at": None,
                "message_id": "56163f81-de30-4c39-b4c4-3a205d0be9da",
                "elements": [
                    {"type": "text", "attrs": {"content": "test"}, "children": []}
                ],
                "timestamp": 1700474858446,
            },
            "operator": None,
            "role": None,
            "user": {
                "id": "3344",
                "name": "Aislinn",
                "nick": None,
                "avatar": "https://img.kookapp.cn/avatars/2021-08/GjdUSjtmtD06j06j.png?x-oss-process=style/icon",
                "is_bot": None,
                "username": "Aislinn",
                "user_id": "3344",
                "discriminator": "4261",
            },
            "_type": "kook",
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="kook",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="6677",
        id3="5566",
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = InternalEvent.parse_obj(
        {
            "id": 4,
            "type": "internal",
            "platform": "kook",
            "self_id": "2233",
            "timestamp": 17000000000,
            "argv": None,
            "button": None,
            "channel": None,
            "guild": None,
            "login": None,
            "member": None,
            "message": None,
            "operator": None,
            "role": None,
            "user": None,
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Satori",
        platform="kook",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
