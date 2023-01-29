from nonebot.adapters.onebot.v11 import (
    NoticeEvent
)
from typing import Literal

class GroupCardNoticeEvent(NoticeEvent):
    """群名片修改事件"""

    notice_type: Literal["group_card"]
    user_id: int
    group_id: int
    card_old: str
    card_new: str
