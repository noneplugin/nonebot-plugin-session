"""delete_duplicate_session

Revision ID: 1d71de778430
Revises: 7d0575ba4608
Create Date: 2023-09-07 19:46:49.978903

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = "1d71de778430"
down_revision = "7d0575ba4608"
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base = automap_base()
    Base.prepare(autoload_with=op.get_bind())
    SessionModel = Base.classes.nonebot_plugin_session_sessionmodel

    session_model_update_set = set()
    with Session(op.get_bind()) as session:
        session_models = session.scalars(
            sa.select(SessionModel).order_by(SessionModel.id)
        ).all()
        for session_model in session_models:
            # 尝试删除重复的 session
            session_data = (
                session_model.bot_id,
                session_model.bot_type,
                session_model.platform,
                session_model.level,
                session_model.id1 or "",
                session_model.id2 or "",
                session_model.id3 or "",
            )
            if session_data in session_model_update_set:
                session.delete(session_model)
            else:
                session_model_update_set.add(session_data)
        session.commit()


def downgrade() -> None:
    pass
