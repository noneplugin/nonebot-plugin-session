from pathlib import Path
from typing import TYPE_CHECKING

import nonebot
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


if TYPE_CHECKING:
    from nonebot.plugin import Plugin


@pytest.fixture(scope="session", autouse=True)
def load_plugin(nonebug_init: None) -> set["Plugin"]:
    # preload global plugins
    return nonebot.load_plugins(str(Path(__file__).parent / "plugins"))
