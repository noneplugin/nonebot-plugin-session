from nonebot import get_driver
from nonebot.adapters.villa import Adapter, Bot
from nonebot.adapters.villa.config import BotInfo
from nonebot.adapters.villa.event import SendMessageEvent
from nonebot.adapters.villa.models import (
    MessageContentInfoGet,
    Robot,
    Template,
    TextMessageContent,
    User,
)
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    return Bot(
        adapter=Adapter(get_driver()),
        self_id=self_id,
        bot_info=BotInfo(
            bot_id=self_id,
            bot_secret="qwerty",
            connection_type="webhook",
            pub_key="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsFPe+wIEc+SuzFrkTMJu\ncIG7XOgJ3FPAXyCPLYQz5pTr8wNydQt910o/bxvFIbeTxczBgsnzFK0J6W8BO7B7\n4kpBeKB017TGWWXaGsd/1Mtf/ZhIamboASFU08/NP4DspkkYGhBwuiDYFQ9AUhlS\nKdAEH5Waw9SqTflGmanaK95F3bJVULomExtqXXk/Yk5sQ6Gala3sFVdzfrti+XzZ\nIANP4S2PG67575w7UaR/FDhhaZWak5mhF49DgTs4kloM2Gf8GDhOxFVQfAm+E3sS\nrDeB6ED0ArfpC9CnG4lw8EkUCKXaRMaELx542W9aFk4x04yS7eeHtR6mO3Bs6mYX\nbQIDAQAB\n-----END PUBLIC KEY-----\n",
        ),
    )


def test_channel_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = SendMessageEvent.parse_obj(
        {
            "robot": Robot(
                villa_id=789, template=Template(id="2233", name="test", icon="qwe")
            ),
            "id": "test_event",
            "send_at": 123456789,
            "created_at": 123456789,
            "content": MessageContentInfoGet(
                content=TextMessageContent(text="test text"),
                user=User(
                    portraitUri="qwe",
                    extra={},
                    name="test",
                    alias="",
                    id="123",
                    portrait="",
                ),
            ).json(by_alias=True),
            "from_user_id": 123,
            "room_id": 456,
            "object_name": 1,
            "nickname": "test",
            "msg_uid": "msg123",
            "villa_id": 789,
        }
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Villa",
        platform="villa",
        level=SessionLevel.LEVEL3,
        id1="123",
        id2="456",
        id3="789",
    )
