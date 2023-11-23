from nonebot.plugin import PluginMetadata

from . import adapters as adapters
from .extractor import EventSession as EventSession
from .extractor import SessionExtractor as SessionExtractor
from .extractor import SessionId as SessionId
from .extractor import extract_session as extract_session
from .session import Session as Session
from .session import SessionIdType as SessionIdType
from .session import SessionLevel as SessionLevel

__plugin_meta__ = PluginMetadata(
    name="会话id",
    description="会话信息提取与会话id定义插件",
    usage="请参考文档",
    type="library",
    homepage="https://github.com/noneplugin/nonebot-plugin-session",
    supported_adapters={
        "~onebot.v11",
        "~onebot.v12",
        "~console",
        "~kaiheila",
        # "~qqguild",
        "~telegram",
        "~feishu",
        "~red",
        "~discord",
        "~qq",
        "~satori",
        "~villa",
        "~dodo",
    },
)
