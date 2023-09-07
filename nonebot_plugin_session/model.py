from typing import List, Union

from .session import Session, SessionIdType, SessionLevel

try:
    from nonebot import require

    require("nonebot_plugin_datastore")

    from nonebot_plugin_datastore import get_plugin_data
    from sqlalchemy import String, UniqueConstraint, exc, select
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
        id1: Mapped[str] = mapped_column(String(64))
        id2: Mapped[str] = mapped_column(String(64))
        id3: Mapped[str] = mapped_column(String(64))

        @property
        def session(self) -> Session:
            return Session(
                bot_id=self.bot_id,
                bot_type=self.bot_type,
                platform=self.platform,
                level=SessionLevel(self.level),
                id1=self.id1 if self.id1 else None,
                id2=self.id2 if self.id2 else None,
                id3=self.id3 if self.id3 else None,
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
                whereclause.append(SessionModel.id1 == (session.id1 or ""))
            if include_id2:
                whereclause.append(SessionModel.id2 == (session.id2 or ""))
            if include_id3:
                whereclause.append(SessionModel.id3 == (session.id3 or ""))
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
            .where(SessionModel.id1 == (session.id1 or ""))
            .where(SessionModel.id2 == (session.id2 or ""))
            .where(SessionModel.id3 == (session.id3 or ""))
        )
        results = await db_session.scalars(statement)
        if session_model := results.one_or_none():
            return session_model

        session_model = SessionModel(
            bot_id=session.bot_id,
            bot_type=session.bot_type,
            platform=session.platform,
            level=session.level,
            id1=session.id1 or "",
            id2=session.id2 or "",
            id3=session.id3 or "",
        )
        if commit:
            # 并发时可能会出现重复插入的情况
            try:
                async with db_session.begin_nested():
                    db_session.add(session_model)
            except exc.IntegrityError:
                session_model = (await db_session.scalars(statement)).one()

        return session_model

except (ImportError, RuntimeError, ModuleNotFoundError):
    pass
