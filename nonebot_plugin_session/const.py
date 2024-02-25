from strenum import StrEnum


class SupportedAdapter(StrEnum):
    console = "Console"
    discord = "Discord"
    dodo = "DoDo"
    feishu = "Feishu"
    kaiheila = "Kaiheila"
    onebot_v11 = "OneBot V11"
    onebot_v12 = "OneBot V12"
    qq = "QQ"
    red = "RedProtocol"
    telegram = "Telegram"


class SupportedPlatform(StrEnum):
    console = "console"
    discord = "discord"
    dodo = "dodo"
    feishu = "feishu"
    kaiheila = "kaiheila"
    qq = "qq"
    qqguild = "qqguild"
    telegram = "telegram"
    unknown = "unknown"
