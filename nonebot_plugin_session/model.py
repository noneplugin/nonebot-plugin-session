from contextlib import asynccontextmanager
from typing import Optional, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from .session import Session, SessionLevel

try:
    from nonebot import require

    require("nonebot_plugin_datastore")

    from nonebot_plugin_datastore import create_session, get_plugin_data
    from sqlalchemy import Enum, String, UniqueConstraint, select
    from sqlalchemy.orm import Mapped, mapped_column

    Model = get_plugin_data().Model

    class SessionModel(Model):
        __table_args__ = (
            UniqueConstraint(
                "bot_id",
                "bot_type",
                "platform",
                "level",
                "id1",
                "id2",
                "id3",
                name="unique_session",
            ),
        )

        id: Mapped[int] = mapped_column(primary_key=True)
        bot_id: Mapped[str] = mapped_column(String(64))
        bot_type: Mapped[str] = mapped_column(String(32))
        platform: Mapped[str] = mapped_column(String(32))
        level: Mapped[SessionLevel] = mapped_column(Enum(SessionLevel))
        id1: Mapped[Optional[str]] = mapped_column(String(64))
        id2: Mapped[Optional[str]] = mapped_column(String(64))
        id3: Mapped[Optional[str]] = mapped_column(String(64))

        @property
        def session(self) -> Session:
            return Session(
                bot_id=self.bot_id,
                bot_type=self.bot_type,
                platform=self.platform,
                level=self.level,
                id1=self.id1,
                id2=self.id2,
                id3=self.id3,
            )


    @asynccontextmanager
    async def _use_or_create_session(session: Optional[AsyncSession]) -> AsyncContextManager[AsyncSession]:
        session_provided = session is not None
        if not session_provided:
            session = create_session()

        try:
            yield session
        finally:
            if not session_provided:
                await session.close()


    async def get_or_add_session_model(session: Session, db_session: Optional[AsyncSession] = None,
                                       commit: bool = True) -> SessionModel:
        session_provided = db_session is not None
        async with _use_or_create_session(db_session) as db_session:
            statement = (
                select(SessionModel)
                .where(SessionModel.bot_id == session.bot_id)
                .where(SessionModel.bot_type == session.bot_type)
                .where(SessionModel.platform == session.platform)
                .where(SessionModel.level == session.level)
                .where(SessionModel.id1 == session.id1)
                .where(SessionModel.id2 == session.id2)
                .where(SessionModel.id3 == session.id3)
            )
            results = await db_session.scalars(statement)
            if session_model := results.one_or_none():
                return session_model

            session_model = SessionModel(
                bot_id=session.bot_id,
                bot_type=session.bot_type,
                platform=session.platform,
                level=session.level,
                id1=session.id1,
                id2=session.id2,
                id3=session.id3,
            )
            db_session.add(session_model)
            if not session_provided or commit:
                await db_session.commit()
                await db_session.refresh(session_model)
            return session_model

except (ImportError, RuntimeError):
    pass
