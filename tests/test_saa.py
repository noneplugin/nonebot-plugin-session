from nonebug.app import App


def test_get_saa_target(app: App):
    from nonebot_plugin_saa.utils.platform_send_target import TargetQQGroup

    from nonebot_plugin_session import Session, SessionLevel

    session = Session(
        bot_id="2233",
        bot_type="OneBot V11",
        platform="qq",
        level=SessionLevel.LEVEL2,
        id1="3344",
        id2="1122",
        id3=None,
    )
    target = session.get_saa_target()
    assert target
    assert isinstance(target, TargetQQGroup)
    assert str(target.group_id) == "1122"
