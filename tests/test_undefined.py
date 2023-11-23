from typing import Any, Union

from nonebot import get_driver
from nonebot.adapters import Adapter, Bot, Event, Message, MessageSegment
from nonebug.app import App
from typing_extensions import override

from .utils import assert_session


class FakeAdapter(Adapter):
    @classmethod
    @override
    def get_name(cls) -> str:
        return "Fake"

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        pass


class FakeBot(Bot):
    adapter: "FakeAdapter"

    @override
    async def send(
        self,
        event: "Event",
        message: Union[str, "Message", "MessageSegment"],
        **kwargs: Any,
    ) -> Any:
        pass


class FakeEvent(Event):
    @override
    def get_type(self) -> str:
        return "message"

    @override
    def get_event_name(self) -> str:
        return "fake"

    @override
    def get_event_description(self) -> str:
        return "fake"

    @override
    def get_user_id(self) -> str:
        raise NotImplementedError

    @override
    def get_session_id(self) -> str:
        raise NotImplementedError

    @override
    def get_message(self) -> "Message":
        raise NotImplementedError

    @override
    def is_tome(self) -> bool:
        raise NotImplementedError


def test_undefined_adapter(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = FakeBot(adapter=FakeAdapter(get_driver()), self_id="2233")
    event = FakeEvent()
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="Fake",
        platform="unknown",
        level=SessionLevel.LEVEL0,
        id1=None,
        id2=None,
        id3=None,
    )
