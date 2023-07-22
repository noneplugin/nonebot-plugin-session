from enum import IntEnum
from typing import TYPE_CHECKING, List, Optional, Union

from pydantic import BaseModel
from strenum import StrEnum

if TYPE_CHECKING:
    try:
        from nonebot_plugin_saa import PlatformTarget
    except ImportError:
        pass


class SessionLevel(StrEnum):
    LEVEL0 = "LEVEL0"
    LEVEL1 = "LEVEL1"
    LEVEL2 = "LEVEL2"
    LEVEL3 = "LEVEL3"


class SessionIdType(IntEnum):
    TYPE0 = 0
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3
    TYPE4 = 4
    TYPE5 = 5
    TYPE6 = 6
    TYPE7 = 7
    GLOBAL = 0
    USER = 1
    GROUP = 6
    GROUP_USER = 7


class Session(BaseModel):
    bot_id: str
    bot_type: str
    platform: str
    level: SessionLevel
    id1: Optional[str]
    id2: Optional[str]
    id3: Optional[str]

    def get_id(
        self,
        id_type: Union[int, SessionIdType],
        *,
        include_platform: bool = True,
        include_bot_type: bool = True,
        include_bot_id: bool = True,
        seperator: str = "_",
    ) -> str:
        id_type = min(max(id_type, 0), SessionIdType.GROUP_USER)

        if self.level == SessionLevel.LEVEL0:
            id_type = 0
        elif self.level == SessionLevel.LEVEL1:
            id_type = int(bool(id_type))
        elif self.level == SessionLevel.LEVEL2:
            id_type = (id_type & 1) | (int(bool(id_type >> 1)) << 1)
        elif self.level == SessionLevel.LEVEL3:
            pass

        include_id1 = bool(id_type & 1)
        include_id2 = bool((id_type >> 1) & 1)
        include_id3 = bool((id_type >> 2) & 1)

        parts: List[str] = []
        if include_platform:
            parts.append(self.platform)
        if include_bot_type:
            parts.append(self.bot_type)
        if include_bot_id:
            parts.append(self.bot_id)
        if include_id3:
            parts.append(self.id3 or "")
        if include_id2:
            parts.append(self.id2 or "")
        if include_id1:
            parts.append(self.id1 or "")

        return seperator.join(parts)

    def get_saa_target(self) -> Optional["PlatformTarget"]:
        raise NotImplementedError
