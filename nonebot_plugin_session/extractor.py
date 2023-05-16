from typing import Generic, List, NamedTuple, Optional, Type, TypeVar, Union

from nonebot.adapters import Bot, Event
from nonebot.params import Depends

from .const import SupportedPlatform
from .session import Session, SessionIdType, SessionLevel

B = TypeVar("B", bound=Bot)
E = TypeVar("E", bound=Event)


class SessionExtractor(Generic[B, E]):
    def __init__(self, bot: B, event: E):
        self.bot = bot
        self.event = event

    def extract_bot_id(self) -> str:
        return self.bot.self_id

    def extract_bot_type(self) -> str:
        return self.bot.type

    def extract_platform(self) -> str:
        return SupportedPlatform.unknown

    def extract_level(self) -> SessionLevel:
        return SessionLevel.LEVEL0

    def extract_id1(self) -> Optional[str]:
        try:
            return self.event.get_user_id()
        except (NotImplementedError, ValueError):
            pass

    def extract_id2(self) -> Optional[str]:
        pass

    def extract_id3(self) -> Optional[str]:
        pass

    def extract(self) -> Session:
        return Session(
            bot_id=self.extract_bot_id(),
            bot_type=self.extract_bot_type(),
            platform=self.extract_platform(),
            level=self.extract_level(),
            id1=self.extract_id1(),
            id2=self.extract_id2(),
            id3=self.extract_id3(),
        )


class SessionExtractorTuple(NamedTuple):
    bot: Type[Bot]
    event: Type[Event]
    extractor: Type[SessionExtractor]


_session_extractors: List[SessionExtractorTuple] = []


def register_session_extractor(bot: Type[Bot], event: Type[Event]):
    def wrapper(extractor: Type[SessionExtractor]):
        _session_extractors.append(SessionExtractorTuple(bot, event, extractor))
        return extractor

    return wrapper


def extract_session(bot: Bot, event: Event) -> Session:
    for extractor_tuple in _session_extractors:
        if isinstance(bot, extractor_tuple.bot) and isinstance(
            event, extractor_tuple.event
        ):
            return extractor_tuple.extractor(bot, event).extract()
    return SessionExtractor(bot, event).extract()


def SessionId(
    id_type: Union[int, SessionIdType],
    *,
    include_platform: bool = True,
    include_bot_type: bool = True,
    include_bot_id: bool = True,
    seperator: str = "_"
):
    def dependency(bot: Bot, event: Event) -> str:
        session = extract_session(bot, event)
        return session.get_id(
            id_type,
            include_platform=include_platform,
            include_bot_type=include_bot_type,
            include_bot_id=include_bot_id,
            seperator=seperator,
        )

    return Depends(dependency)
