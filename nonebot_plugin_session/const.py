from strenum import StrEnum


class SupportedAdapter(StrEnum):
    onebot_v11 = "OneBot V11"
    onebot_v12 = "OneBot V12"
    console = "Console"
    kaiheila = "Kaiheila"
    qqguild = "QQ Guild"


class SupportedPlatform(StrEnum):
    qq = "qq"
    console = "console"
    kaiheila = "kaiheila"
    qqguild = "qqguild"
    unknown = "unknown"
