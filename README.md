<div align="center">

  <a href="https://v2.nonebot.dev/">
    <img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot">
  </a>

# nonebot-plugin-session

_✨ [Nonebot2](https://github.com/nonebot/nonebot2) 会话信息提取与会话 id 定义插件 ✨_

<p align="center">
  <img src="https://img.shields.io/github/license/noneplugin/nonebot-plugin-session" alt="license">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/nonebot-2.0.0+-red.svg" alt="NoneBot">
  <a href="https://pypi.org/project/nonebot-plugin-session">
    <img src="https://badgen.net/pypi/v/nonebot-plugin-session" alt="pypi">
  </a>
</p>

</div>


- 这个插件可以做什么？

本插件提供了一个统一的会话模型 `Session`，
可以从不同适配器的 `Bot` 和 `Event` 中提取与会话相关的
“平台”、“会话等级”（单用户、单级群组、两级群组）、“目标 id” 等属性；

同时提供了获取会话 id 的函数，可以按照不同的类型获取会话id，方便不同场景下的使用

- 这个插件解决了什么问题？

Nonebot 适配器基类中提供了 `get_session_id` 函数用于获取会话 id，
但这一结果通常是 用户 id、群组 id 的组合，属于 “用户级别” 的 id，
但在很多插件中，需要用到 “群组级别” 的会话 id，如词云、词库等等

本插件可以为不同适配器提供一个统一的、可选级别的会话 id 定义方式


### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_session
```

- 使用 pip

```
pip install nonebot_plugin_session
```

### 使用


获取 `Session`：

```python
from nonebot_plugin_session import extract_session

@matcher.handle()
async def handle(bot: Bot, event: Event):
    session = extract_session(bot, event)
```


获取 `session id`：

```python
from nonebot_plugin_session import SessionId, SessionIdType

@matcher.handle()
async def handle(session_id: str = SessionId(SessionIdType.GROUP)):
    # 获取 “群组级别” 的 session id
    ...
```


将 `Session` 存至数据库中（需要安装 [nonebot-plugin-datastore](https://github.com/he0119/nonebot-plugin-datastore) 插件）

```python
from nonebot_plugin_datastore import create_session
from nonebot_plugin_session import extract_session
from nonebot_plugin_session.model import get_or_add_session_model

@matcher.handle()
async def handle(bot: Bot, event: Event):
    session = extract_session(bot, event)
    async with create_session() as db_session:
        session_model = await get_or_add_session_model(session, db_session)  # 可关联其他表用于筛选等
```


从 `Session` 中获取 `saa` 的 `PlatformTarget` 对象用于发送（需要安装 [nonebot-plugin-send-anything-anywhere](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere) 插件）

```python
from nonebot_plugin_session import extract_session

@matcher.handle()
async def handle(bot: Bot, event: Event):
    session = extract_session(bot, event)
    target = session.get_saa_target()  # 用于发送
```


不同的 “会话级别” 与 “会话id类型” 下返回的 id 如下表所示：（不包含 `bot_id` 等属性的情况）

| | LEVEL0<br>（无用户） | LEVEL1<br>（单用户） | LEVEL2<br>（单级群组） | LEVEL3<br>（两级群组） | 
| --- | --- | --- | --- | --- |
| TYPE0 (GLOBAL) | `""` | `""` | `""` | `""` |
| TYPE1 (USER) | `""` | `"id1"` | `"id1"` | `"id1"` |
| TYPE2 | `""` | `"id1"` | `"id2"` | `"id2"` |
| TYPE3 | `""` | `"id1"` | `"id2_id1"` | `"id2_id1"` |
| TYPE4 | `""` | `"id1"` | `"id2"` | `"id3"` |
| TYPE5 | `""` | `"id1"` | `"id2_id1"` | `"id3_id1"` |
| TYPE6 (GROUP) | `""` | `"id1"` | `"id2"` | `"id3_id2"` |
| TYPE7 (GROUP_USER) | `""` | `"id1"` | `"id2_id1"` | `"id3_id2_id1"` |


### 支持的 adapter

| OneBot v11 | OneBot v12 | Console | Kaiheila | QQ Guild | Telegram |
| :--------: | :--------: | :------: | :------: | :------: | :------: |
|     ✅     |     ✅     |    ✅    |    ✅    |    ✅    |    ✅    |


### 鸣谢

- [nonebot-plugin-send-anything-anywhere](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere) 项目的灵感来源以及部分实现的参考
- [uy/sun](https://github.com/he0119) 感谢歪日佬的技术支持
