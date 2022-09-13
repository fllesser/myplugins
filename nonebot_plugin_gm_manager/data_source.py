import time, asyncio
from nonebot.adapters.onebot.v11 import Bot
from typing import Dict, List, Any

from services.log import logger

from .model import GroupInfoUserByMe


async def kick_not_active_member(bot: Bot, group_id: int, kicked_num: int) -> str:
    members = await get_kicked_list(bot=bot, group_id=group_id, kicked_num=kicked_num)
    if members is None or members == []:
        return "没有需要清理(即符合设置的规则)的成员, 请修改规则"
    message_str = ""
    for member in members:
        await bot.set_group_kick(group_id=group_id, user_id=member["user_id"])
        await GroupInfoUserByMe.delete_member_info(user_qq=member["user_id"], group_id=group_id)
        logger.info(f"{member} -> kicked")
        message_str += f"{member['user_id']} {(member['card'] if not member['card'] == '' else member['nickname'])}\n"
        await asyncio.sleep(1)
    return f"{message_str}通通被我送走了捏"


async def get_kicked_list(bot: Bot, group_id: int, kicked_num: int) -> List[Dict[str, Any]]:
    # 待踢群员列表
    members = []
    # 初始化
    if GroupInfoUserByMe.query_start_dict.get(str(group_id)) is None:
        GroupInfoUserByMe.query_start_dict[str(group_id)] = 1
    now_time = int(time.time())
    for i in range(GroupInfoUserByMe.query_start_dict[str(group_id)], 20):
        try:
            gm_list = await GroupInfoUserByMe.get_group_user_qq_list(
                group_id=group_id,
                user_num=100,
                off_set=(i - 1) * 100 + 1
            )        
        except:
            return members
        for member_qq in gm_list:
            try:
                member = await bot.get_group_member_info(user_id=member_qq, group_id=group_id, no_cache=True)
            except:
                await GroupInfoUserByMe.delete_member_info(user_qq=member_qq, group_id=group_id)
                continue
            if (now_time - int(member["last_sent_time"]) > 7777777) and int(member["level"]) < 20:
                members.append(member)
            if len(members) == kicked_num:
                return members
        logger.info(f"当前查询第{i}页, 已匹配的待踢人数{len(members)}")
        if len(members) == 0:
            GroupInfoUserByMe.query_start_dict[str(group_id)] += 1
