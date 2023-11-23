from nonebug.app import App

from .utils import assert_session_id


async def test_session_id(app: App):
    from nonebot_plugin_session import Session, SessionLevel

    session = Session(
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

    session = Session(
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

    session = Session(
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

    session = Session(
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL3,
        id1="3344",
        id2="1122",
        id3="5566",
    )
    assert_session_id(
        session,
        (
            "qq_OneBot V11_2233",
            "qq_OneBot V11_2233_3344",
            "qq_OneBot V11_2233_1122",
            "qq_OneBot V11_2233_1122_3344",
            "qq_OneBot V11_2233_5566",
            "qq_OneBot V11_2233_5566_3344",
            "qq_OneBot V11_2233_5566_1122",
            "qq_OneBot V11_2233_5566_1122_3344",
        ),
    )


async def test_event_session(app: App):
    from nonebot import get_driver
    from nonebot.adapters.onebot.v11 import Adapter, Bot, Message, PrivateMessageEvent
    from nonebot.adapters.onebot.v11.event import Sender

    from nonebot_plugin_session import Session, SessionLevel

    def _private_message_event(message: str) -> PrivateMessageEvent:
        return PrivateMessageEvent(
            time=1122,
            self_id=2233,
            post_type="message",
            sub_type="",
            user_id=3344,
            message_id=4455,
            message=Message(message),
            original_message=Message(message),
            message_type="private",
            raw_message=message,
            font=1,
            sender=Sender(user_id=3344),
        )

    async with app.test_matcher() as ctx:
        bot = ctx.create_bot(base=Bot, adapter=Adapter(get_driver()), self_id="2233")

        event = _private_message_event("/session")
        session = Session(
            bot_id="2233",
            bot_type="OneBot V11",
            platform="qq",
            level=SessionLevel.LEVEL1,
            id1="3344",
            id2=None,
            id3=None,
        )
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "", True, session=session)

        event = _private_message_event("/session_id")
        session_id = "qq_OneBot V11_2233_3344"
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, session_id, True)
