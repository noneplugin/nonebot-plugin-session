"""set not null value

Revision ID: 4a6b4ef804a9
Revises: 1d71de778430
Create Date: 2023-09-07 19:49:49.212664

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = "4a6b4ef804a9"
down_revision = "1d71de778430"
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base = automap_base()
    Base.prepare(autoload_with=op.get_bind())
    SessionModel = Base.classes.nonebot_plugin_session_sessionmodel

    with Session(op.get_bind()) as session:
        session_models = session.scalars(sa.select(SessionModel)).all()
        for session_model in session_models:
            if session_model.id1 is None:
                session_model.id1 = ""
            if session_model.id2 is None:
                session_model.id2 = ""
            if session_model.id3 is None:
                session_model.id3 = ""

        session.add_all(session_models)
        session.commit()


def downgrade() -> None:
    pass
