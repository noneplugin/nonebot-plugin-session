from nonebot import on_command, require

require("nonebot_plugin_session")

from nonebot_plugin_session import EventSession, SessionId, SessionIdType

session_cmd = on_command("session")


@session_cmd.handle()
async def _(session: EventSession):
    await session_cmd.send("", session=session)


session_id_cmd = on_command("session_id")


@session_id_cmd.handle()
async def _(
    session_id: str = SessionId(SessionIdType.GROUP_USER),
):
    await session_id_cmd.send(session_id)
