from typing import Optional

from .const import SupportedAdapter, SupportedPlatform
from .session import Session, SessionLevel

try:
    from nonebot import require

    require("nonebot_plugin_saa")

    from nonebot_plugin_saa import (
        PlatformTarget,
        TargetKaiheilaChannel,
        TargetKaiheilaPrivate,
        TargetOB12Unknow,
        TargetQQGroup,
        TargetQQGuildChannel,
        TargetQQGuildDirect,
        TargetQQPrivate,
    )

    def get_saa_target(self: Session) -> Optional[PlatformTarget]:
        if self.platform == SupportedPlatform.qq:
            if self.level == SessionLevel.LEVEL1 and self.id1:
                return TargetQQPrivate(user_id=int(self.id1))
            elif self.level == SessionLevel.LEVEL2 and self.id2:
                return TargetQQGroup(group_id=int(self.id2))

        elif self.platform == SupportedPlatform.qqguild:
            if self.level == SessionLevel.LEVEL1:
                if self.id1 and self.id3:
                    return TargetQQGuildDirect(
                        recipient_id=int(self.id1), source_guild_id=int(self.id3)
                    )
            elif self.level == SessionLevel.LEVEL3:
                if self.id2:
                    return TargetQQGuildChannel(channel_id=int(self.id2))

        elif self.platform == SupportedPlatform.kaiheila:
            if self.level == SessionLevel.LEVEL1 and self.id1:
                return TargetKaiheilaPrivate(user_id=self.id1)
            if self.level == SessionLevel.LEVEL3 and self.id2:
                return TargetKaiheilaChannel(channel_id=self.id2)

        if self.bot_type == SupportedAdapter.onebot_v12:
            if self.level == SessionLevel.LEVEL1:
                return TargetOB12Unknow(detail_type="private", user_id=self.id1)
            elif self.level == SessionLevel.LEVEL2:
                return TargetOB12Unknow(detail_type="group", group_id=self.id2)
            elif self.level == SessionLevel.LEVEL3:
                return TargetOB12Unknow(
                    detail_type="channel", channel_id=self.id2, guild_id=self.id3
                )

    Session.get_saa_target = get_saa_target
except (ImportError, RuntimeError, ModuleNotFoundError):
    pass
