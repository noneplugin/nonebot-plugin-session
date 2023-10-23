from nonebot import get_driver
from nonebot.adapters.feishu import (
    Adapter,
    Bot,
    EventHeader,
    GroupMessageEvent,
    GroupMessageEventDetail,
    MessageReadEvent,
    MessageReadEventDetail,
    PrivateMessageEvent,
    PrivateMessageEventDetail,
    UserId,
)
from nonebot.adapters.feishu.bot import BotInfo
from nonebot.adapters.feishu.config import BotConfig
from nonebot.adapters.feishu.models import (
    GroupEventMessage,
    MessageReader,
    PrivateEventMessage,
    Sender,
)
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    bot_config = BotConfig(app_id="114", app_secret="514", verification_token="1919810")
    bot_info = BotInfo.parse_obj(
        {
            "activate_status": 2,
            "app_name": "name",
            "avatar_url": "https://s1-imfile.feishucdn.com/test.jpg",
            "ip_white_list": [],
            "open_id": "ou_123456",
        }
    )

    return Bot(
        adapter=Adapter(get_driver()),
        self_id=self_id,
        bot_config=bot_config,
        bot_info=bot_info,
    )


def test_private_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    header = EventHeader(
        event_id="114514",
        event_type="im.message.receive_v1",
        create_time="123456",
        token="token",
        app_id="app_id",
        tenant_key="tenant_key",
        resource_id=None,
        user_list=None,
    )
    sender = Sender(
        sender_id=UserId(
            open_id="3344",
            user_id="on_111",
            union_id="on_222",
        ),
        tenant_key="tenant_key",
        sender_type="user",
    )
    event = PrivateMessageEvent(
        schema="2.0",
        header=header,
        event=PrivateMessageEventDetail(
            sender=sender,
            message=PrivateEventMessage(
                chat_type="p2p",
                message_id="om_111",
                root_id="om_222",
                parent_id="om_333",
                create_time="123456",
                chat_id="oc_123",
                message_type="text",
                content='{"text":"hello"}',  # type: ignore
                mentions=None,
            ),
        ),
        reply=None,
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Feishu",
        platform="feishu",
        level=SessionLevel.LEVEL1,
        id1="3344",
        id2=None,
        id3=None,
    )


def test_group_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    header = EventHeader(
        event_id="114514",
        event_type="im.message.receive_v1",
        create_time="123456",
        token="token",
        app_id="app_id",
        tenant_key="tenant_key",
        resource_id=None,
        user_list=None,
    )
    sender = Sender(
        sender_id=UserId(
            open_id="3344",
            user_id="on_111",
            union_id="on_222",
        ),
        tenant_key="tenant_key",
        sender_type="user",
    )
    event = GroupMessageEvent(
        schema="2.0",
        header=header,
        event=GroupMessageEventDetail(
            sender=sender,
            message=GroupEventMessage(
                chat_type="group",
                message_id="om_111",
                root_id="om_222",
                parent_id="om_333",
                create_time="123456",
                chat_id="1122",
                message_type="text",
                content='{"text":"hello"}',  # type: ignore
                mentions=None,
            ),
        ),
        reply=None,
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Feishu",
        platform="feishu",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="1122",
        id3=None,
    )


def test_undefined_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    header = EventHeader(
        event_id="114514",
        event_type="im.message.receive_v1",
        create_time="123456",
        token="token",
        app_id="app_id",
        tenant_key="tenant_key",
        resource_id=None,
        user_list=None,
    )
    event = MessageReadEvent(
        schema="2.0",
        header=header,
        event=MessageReadEventDetail(
            reader=MessageReader(
                reader_id=UserId(
                    open_id="3344",
                    user_id="on_111",
                    union_id="on_222",
                ),
                read_time="123456",
                tenant_key="tenant_key",
            ),
            message_id_list=["114514"],
        ),
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Feishu",
        platform="feishu",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
