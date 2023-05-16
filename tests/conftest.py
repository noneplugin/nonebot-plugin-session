from pathlib import Path

import pytest
from nonebot import require
from nonebug import NONEBOT_INIT_KWARGS, App
from sqlalchemy import StaticPool, delete


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~websockets",
        "datastore_database_url": "sqlite+aiosqlite://",
        "datastore_engine_options": {"poolclass": StaticPool},
    }


@pytest.fixture
async def app(tmp_path: Path):
    require("nonebot_plugin_session")

    from nonebot_plugin_datastore.config import plugin_config
    from nonebot_plugin_datastore.db import create_session, init_db

    plugin_config.datastore_cache_dir = tmp_path / "cache"
    plugin_config.datastore_config_dir = tmp_path / "config"
    plugin_config.datastore_data_dir = tmp_path / "data"

    await init_db()
    yield App()

    from nonebot_plugin_session.model import SessionModel

    async with create_session() as session, session.begin():
        await session.execute(delete(SessionModel))
