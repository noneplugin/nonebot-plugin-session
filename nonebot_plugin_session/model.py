from typing import Optional

from .session import Session, SessionLevel

try:
    from nonebot import require

    require("nonebot_plugin_datastore")

    from nonebot_plugin_datastore import get_plugin_data
    from sqlalchemy import String, UniqueConstraint, select
    from sqlalchemy.ext.asyncio import AsyncSession
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
        level: Mapped[str] = mapped_column(String(6))
        id1: Mapped[Optional[str]] = mapped_column(String(64))
        id2: Mapped[Optional[str]] = mapped_column(String(64))
        id3: Mapped[Optional[str]] = mapped_column(String(64))

        @property
        def session(self) -> Session:
            return Session(
                bot_id=self.bot_id,
                bot_type=self.bot_type,
                platform=self.platform,
                level=SessionLevel(self.level),
                id1=self.id1,
                id2=self.id2,
                id3=self.id3,
            )

    async def get_or_add_session_model(
        session: Session, db_session: AsyncSession, commit: bool = True
    ) -> SessionModel:
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
        if commit:
            await db_session.commit()
            await db_session.refresh(session_model)
        return session_model

except (ImportError, RuntimeError, ModuleNotFoundError):
    pass
