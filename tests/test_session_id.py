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
