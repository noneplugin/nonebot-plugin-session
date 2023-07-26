from typing import List, Optional, Union

from .session import Session, SessionIdType, SessionLevel

try:
    from nonebot import require

    require("nonebot_plugin_datastore")

    from nonebot_plugin_datastore import get_plugin_data
    from sqlalchemy import String, UniqueConstraint, select
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import Mapped, mapped_column
    from sqlalchemy.sql import ColumnElement

    plugin_data = get_plugin_data()
    plugin_data.use_global_registry()
    Model = plugin_data.Model

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

        @staticmethod
        def filter_statement(
            session: Session,
            id_type: Union[int, SessionIdType],
            *,
            include_platform: bool = True,
            include_bot_type: bool = True,
            include_bot_id: bool = True,
        ) -> List[ColumnElement[bool]]:
            id_type = min(max(id_type, 0), SessionIdType.GROUP_USER)

            if session.level == SessionLevel.LEVEL0:
                id_type = 0
            elif session.level == SessionLevel.LEVEL1:
                id_type = int(bool(id_type))
            elif session.level == SessionLevel.LEVEL2:
                id_type = (id_type & 1) | (int(bool(id_type >> 1)) << 1)
            elif session.level == SessionLevel.LEVEL3:
                pass

            include_id1 = bool(id_type & 1)
            include_id2 = bool((id_type >> 1) & 1)
            include_id3 = bool((id_type >> 2) & 1)

            whereclause: List[ColumnElement[bool]] = []
            if include_bot_id:
                whereclause.append(SessionModel.bot_id == session.bot_id)
            if include_bot_type:
                whereclause.append(SessionModel.bot_type == session.bot_type)
            if include_platform:
                whereclause.append(SessionModel.platform == session.platform)
            if include_id1:
                whereclause.append(SessionModel.id1 == session.id1)
            if include_id2:
                whereclause.append(SessionModel.id2 == session.id2)
            if include_id3:
                whereclause.append(SessionModel.id3 == session.id3)
            return whereclause

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
