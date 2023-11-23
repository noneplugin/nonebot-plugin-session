from nonebot.plugin import PluginMetadata

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
    },
)
