from typing import Optional

from .const import SupportedAdapter, SupportedPlatform
from .session import Session, SessionLevel

try:
    from nonebot_plugin_saa import (  # TargetKaiheilaChannel,; TargetKaiheilaPrivate,; TargetQQGuildChannel,; TargetQQGuildDirect,
        PlatformTarget,
        TargetOB12Unknow,
        TargetQQGroup,
        TargetQQPrivate,
    )

    def get_saa_target_from_session(session: Session) -> Optional[PlatformTarget]:
        if session.platform == SupportedPlatform.qq:
            if session.level == SessionLevel.LEVEL0 and session.id1:
                return TargetQQPrivate(user_id=int(session.id1))
            elif session.level == SessionLevel.LEVEL1 and session.id2:
                return TargetQQGroup(group_id=int(session.id2))

        # elif session.platform == SupportedPlatform.qqguild:
        #     if session.level == SessionLevel.LEVEL3:
        #         if session.id2:
        #             return TargetQQGuildChannel(channel_id=int(session.id2))
        #         if session.id1 and session.id3:
        #             return TargetQQGuildDirect(
        #                 recipient_id=int(session.id1), source_guild_id=int(session.id3)
        #             )

        # elif session.platform == SupportedPlatform.kaiheila:
        #     if session.level == SessionLevel.LEVEL1 and session.id1:
        #         return TargetKaiheilaPrivate(user_id=session.id1)
        #     if session.level == SessionLevel.LEVEL3 and session.id2:
        #         return TargetKaiheilaChannel(channel_id=session.id2)

        if session.bot_type == SupportedAdapter.onebot_v12:
            if session.level == SessionLevel.LEVEL1:
                return TargetOB12Unknow(detail_type="private", user_id=session.id1)
            elif session.level == SessionLevel.LEVEL2:
                return TargetOB12Unknow(detail_type="group", group_id=session.id2)
            elif session.level == SessionLevel.LEVEL3:
                return TargetOB12Unknow(
                    detail_type="channel", channel_id=session.id2, guild_id=session.id3
                )

except ImportError:
    pass
