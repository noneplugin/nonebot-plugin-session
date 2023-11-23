from nonebot import get_driver
from nonebot.adapters.red import Adapter, Bot, Message
from nonebot.adapters.red.api.model import ChatType, MsgType, RoleInfo
from nonebot.adapters.red.config import BotInfo
from nonebot.adapters.red.event import (
    GroupMessageEvent,
    NoticeEvent,
    PrivateMessageEvent,
)
from nonebug.app import App

from .utils import assert_session


def new_bot(self_id: str) -> Bot:
    return Bot(
        adapter=Adapter(get_driver()),
        self_id=self_id,
        info=BotInfo(port=1234, token="1234"),
    )


def test_private_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    message = Message("test")
    event = PrivateMessageEvent(
        message=message,
        original_message=message,
        msgId="7272944767457625851",
        msgRandom="196942265",
        msgSeq="103",
        cntSeq="0",
        chatType=ChatType.FRIEND,
        msgType=MsgType.normal,
        subMsgType=1,
        sendType=0,
        senderUid="4321",
        senderUin="1234",
        peerUid="4321",
        peerUin="1234",
        channelId="",
        guildId="",
        guildCode="0",
        fromUid="0",
        fromAppid="0",
        msgTime="1693364414",
        msgMeta="0x",
        sendStatus=2,
        sendMemberName="",
        sendNickName="",
        guildName="",
        channelName="",
        elements=[],
        records=[],
        emojiLikesList=[],
        commentCnt="0",
        directMsgFlag=0,
        directMsgMembers=[],
        peerName="",
        editable=False,
        avatarMeta="",
        avatarPendant="",
        feedId="",
        roleId="0",
        timeStamp="0",
        isImportMsg=False,
        atType=0,
        roleType=0,
        fromChannelRoleInfo=RoleInfo(roleId="0", name="", color=0),
        fromGuildRoleInfo=RoleInfo(roleId="0", name="", color=0),
        levelRoleInfo=RoleInfo(roleId="0", name="", color=0),
        recallTime="0",
        isOnlineMsg=True,
        generalFlags="0x",
        clientSeq="27516",
        nameType=0,
        avatarFlag=0,
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="RedProtocol",
        platform="qq",
        level=SessionLevel.LEVEL1,
        id1="1234",
        id2=None,
        id3=None,
    )


def test_group_message_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    message = Message("test")
    event = GroupMessageEvent(
        message=message,
        original_message=message,
        msgId="7272944513098472702",
        msgRandom="1526531828",
        msgSeq="831",
        cntSeq="0",
        chatType=ChatType.GROUP,
        msgType=MsgType.normal,
        subMsgType=1,
        sendType=0,
        senderUid="4321",
        senderUin="1234",
        peerUid="1111",
        peerUin="1111",
        channelId="",
        guildId="",
        guildCode="0",
        fromUid="0",
        fromAppid="0",
        msgTime="1693364354",
        msgMeta="0x",
        sendStatus=2,
        sendMemberName="",
        sendNickName="uy/sun",
        guildName="",
        channelName="",
        elements=[],
        records=[],
        emojiLikesList=[],
        commentCnt="0",
        directMsgFlag=0,
        directMsgMembers=[],
        peerName="uy/sun",
        editable=False,
        avatarMeta="",
        avatarPendant="",
        feedId="",
        roleId="0",
        timeStamp="0",
        isImportMsg=False,
        atType=0,
        roleType=None,
        fromChannelRoleInfo=RoleInfo(roleId="0", name="", color=0),
        fromGuildRoleInfo=RoleInfo(roleId="0", name="", color=0),
        levelRoleInfo=RoleInfo(roleId="0", name="", color=0),
        recallTime="0",
        isOnlineMsg=True,
        generalFlags="0x",
        clientSeq="0",
        nameType=0,
        avatarFlag=0,
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="RedProtocol",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="1234",
        id2="1111",
        id3=None,
    )


def test_notice_event(app: App):
    from nonebot_plugin_session import SessionLevel, extract_session

    bot = new_bot(self_id="2233")
    event = NoticeEvent(
        msgId="7272944513098472702",
        msgRandom="1526531828",
        msgSeq="831",
        cntSeq="0",
        chatType=ChatType.GROUP,
        msgType=MsgType.normal,
        subMsgType=1,
        peerUid="1111",
        peerUin="1111",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="RedProtocol",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1=None,
        id2="1111",
        id3=None,
    )

    event = NoticeEvent(
        msgId="7272944513098472702",
        msgRandom="1526531828",
        msgSeq="831",
        cntSeq="0",
        chatType=ChatType.FRIEND,
        msgType=MsgType.normal,
        subMsgType=1,
        peerUid="1111",
        peerUin="1111",
    )
    session = extract_session(bot, event)
    assert_session(
        session,
        bot_id="2233",
        bot_type="RedProtocol",
        platform="qq",
        level=SessionLevel.LEVEL1,
        id1=None,
        id2=None,
        id3=None,
    )
