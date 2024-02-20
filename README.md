<div align="center">

  <a href="https://nonebot.dev/">
    <img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot">
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

本插件提供了一个统一的会话模型 `Session`，可以从不同适配器的 `Bot` 和 `Event` 中提取与会话相关的属性

具体定义如下：

| 属性       | 类型      | 含义                     | 备注                                                                                     |
| ---------- | --------- | ------------------------ | ---------------------------------------------------------------------------------------- |
| `bot_id`   | `str`     | 机器人 id                |                                                                                          |
| `bot_type` | `str`     | 机器人类型（适配器名称） |                                                                                          |
| `platform` | `str`     | 平台                     | 未知平台用 `unknown` 表示                                                                |
| `level`    | `IntEnum` | 会话等级                 | 目前分为 LEVEL0（无用户）、LEVEL1（单用户）、LEVEL2（单级群组）、LEVEL3（两级群组） 四类 |
| `id1`      | `str`     | 1 级 id                  | 通常为 `user_id`                                                                         |
| `id2`      | `str`     | 2 级 id                  | 通常为 单级群组中的 `group_id`，两级群组中的 `channel_id`                                |
| `id3`      | `str`     | 3 级 id                  | 通常为 两级群组中的 `guild_id`                                                           |

同时，本插件提供了获取会话 id 的函数，可以按照不同的类型获取会话id，方便不同场景下的使用

Nonebot 适配器基类中也提供了 `get_session_id` 函数，但通常是 用户 id、群组 id 的组合，属于 “用户级别” 的 id，很多插件中需要用到不同级别的会话 id，如词云、词库等等

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

#### 获取 `Session`：

```python
from nonebot_plugin_session import extract_session

@matcher.handle()
async def handle(bot: Bot, event: Event):
    session = extract_session(bot, event)
```

或使用依赖注入的形式：

```python
from nonebot_plugin_session import EventSession

@matcher.handle()
async def handle(session: EventSession):
    ...
```

#### 获取 `session id`：

```python
from nonebot_plugin_session import extract_session, SessionIdType

@matcher.handle()
async def handle(bot: Bot, event: Event):
    session = extract_session(bot, event)
    session_id = session.get_id(SessionIdType.GROUP)  # 获取 “群组级别” 的 session id
```

或使用依赖注入的形式：

```python
from nonebot_plugin_session import SessionId, SessionIdType

@matcher.handle()
async def handle(session_id: str = SessionId(SessionIdType.GROUP)):
    ...
```

不同的 “会话级别” 与 “会话id类型” 下返回的 id 如下表所示：（不包含 `bot_id` 等属性的情况）

|                    | LEVEL0<br>（无用户） | LEVEL1<br>（单用户） | LEVEL2<br>（单级群组） | LEVEL3<br>（两级群组） |
| ------------------ | -------------------- | -------------------- | ---------------------- | ---------------------- |
| TYPE0 (GLOBAL)     | `""`                 | `""`                 | `""`                   | `""`                   |
| TYPE1 (USER)       | `""`                 | `"id1"`              | `"id1"`                | `"id1"`                |
| TYPE2              | `""`                 | `"id1"`              | `"id2"`                | `"id2"`                |
| TYPE3              | `""`                 | `"id1"`              | `"id2_id1"`            | `"id2_id1"`            |
| TYPE4              | `""`                 | `"id1"`              | `"id2"`                | `"id3"`                |
| TYPE5              | `""`                 | `"id1"`              | `"id2_id1"`            | `"id3_id1"`            |
| TYPE6 (GROUP)      | `""`                 | `"id1"`              | `"id2"`                | `"id3_id2"`            |
| TYPE7 (GROUP_USER) | `""`                 | `"id1"`              | `"id2_id1"`            | `"id3_id2_id1"`        |

### 支持的 adapter

- [x] OneBot v11
- [x] OneBot v12
- [x] Console
- [x] Kaiheila
- [x] Telegram
- [x] Feishu
- [x] RedProtocol
- [x] Discord
- [x] QQ
- [x] Satori
- [x] DoDo

### 相关插件

- [nonebot-plugin-session-orm](https://github.com/noneplugin/nonebot-plugin-session-orm) 为 session 提供数据库模型及存取方法
- [nonebot-plugin-session-saa](https://github.com/noneplugin/nonebot-plugin-session-saa) 提供从 session 获取 [saa](https://github.com/MountainDash/nonebot-plugin-send-anything-anywhere) 发送对象 [PlatformTarget](https://github.com/MountainDash/nonebot-plugin-send-anything-anywhere/blob/main/nonebot_plugin_saa/utils/platform_send_target.py) 的方法

### 鸣谢

- [nonebot-plugin-send-anything-anywhere](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere) 项目的灵感来源以及部分实现的参考
- [uy/sun](https://github.com/he0119) 感谢歪日佬的技术支持
