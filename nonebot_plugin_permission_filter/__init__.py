from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, GroupIncreaseNoticeEvent
from nonebot import on_command

__zx_plugin_name__ = "权限过滤器"

permission_filter = on_command(cmd="ban", aliases={"禁", "kick", "踢", "kugm"}, priority=9, block=False)

@permission_filter.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if (await bot.get_group_member_info(user_id=event.user_id, group_id=event.group_id, no_cache=True))["role"] == "member":
        await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=60)