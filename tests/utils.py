from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from nonebot_plugin_session import Session, SessionLevel


def assert_session(
    session: "Session",
    *,
    bot_id: str,
    bot_type: str,
    platform: str,
    level: "SessionLevel",
    id1: Optional[str],
    id2: Optional[str],
    id3: Optional[str],
):
    assert session.bot_id == bot_id
    assert session.bot_type == bot_type
    assert session.platform == platform
    assert session.level == level
    assert session.id1 == id1
    assert session.id2 == id2
    assert session.id3 == id3


def assert_session_id(session: "Session", ids: tuple[str, ...]):
    for i in range(len(ids)):
        assert session.get_id(i) == ids[i]
