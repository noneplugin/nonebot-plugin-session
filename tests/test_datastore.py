from nonebug.app import App
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import assert_session


async def test_create_session(app: App):
    from nonebot_plugin_datastore import create_session

    from nonebot_plugin_session import Session, SessionLevel
    from nonebot_plugin_session.model import get_or_add_session_model

    session = Session(
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="1122",
        id3=None,
    )

    async with create_session() as db_session:
        session_model = await get_or_add_session_model(session, db_session)
        assert session_model.id != 0
        assert AsyncSession.object_session(session_model) == db_session.sync_session
        assert_session(
            session_model.session,
            bot_id="2233",
            bot_type="OneBot V11",
            platform="qq",
            level=SessionLevel.LEVEL2,
            id1="3344",
            id2="1122",
            id3=None,
        )


async def test_create_and_filter_session(app: App):
    from nonebot_plugin_datastore import create_session

    from nonebot_plugin_session import Session, SessionLevel
    from nonebot_plugin_session.model import SessionModel, get_or_add_session_model

    session = Session(
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="1122",
        id3=None,
    )

    async with create_session() as db_session:
        session_model = await get_or_add_session_model(session, db_session)
        assert session_model.id != 0

        statement = select(SessionModel).where(
            SessionModel.bot_id == "2233",
            SessionModel.level == SessionLevel.LEVEL2,
            SessionModel.id2 == "1122",
        )
        results = await db_session.scalars(statement)
        session_models = results.all()
        assert session_models
        assert len(session_models) == 1
        session_model = session_models[0]
        assert_session(
            session_model.session,
            bot_id="2233",
            bot_type="OneBot V11",
            platform="qq",
            level=SessionLevel.LEVEL2,
            id1="3344",
            id2="1122",
            id3=None,
        )
