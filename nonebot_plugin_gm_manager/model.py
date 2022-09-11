from typing import ClassVar, List

from models.group_member_info import GroupInfoUser

class GroupInfoUserByMe(GroupInfoUser):

    query_start_dict = {"23213":1}

    @classmethod
    async def get_group_user_qq_list(cls, group_id: int, user_num: int, off_set: int) -> List[int]:
        """
        说明:
            获取该群指定数量用户qq
        参数:
            :param group_id: 群号
             user_num: 要获取的用户qq数量
             off_set: 从哪行开始
        """
        member_list = []
        query = cls.query.where((cls.group_id == group_id)).limit(user_num).offset(off_set - 1)
        for user in await query.gino.all():
            member_list.append(user.user_qq)
        return member_list