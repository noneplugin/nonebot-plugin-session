import pytest
from nonebot import require
from nonebug import NONEBOT_INIT_KWARGS, App


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~websockets+~httpx",
    }


@pytest.fixture
async def app():
    require("nonebot_plugin_session")

    yield App()
