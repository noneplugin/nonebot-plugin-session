from nonebug.app import App
from sqlalchemy import select


async def test_create_and_filter_session(app: App):
    from nonebot_plugin_datastore import create_session

    from nonebot_plugin_session import Session, SessionLevel
    from nonebot_plugin_session.model import SessionModel, get_or_create_session_model

    session = Session(
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="1122",
        id3=None,
    )
    await get_or_create_session_model(session)
    async with create_session() as db_session:
        statement = select(SessionModel).where(
            SessionModel.bot_id == "2233",
            SessionModel.level == SessionLevel.LEVEL2,
            SessionModel.id2 == "1122",
        )
        results = await db_session.scalars(statement)
        session_model = results.all()
        assert session_model
        assert len(session_model) == 1
