from nonebot.adapters.onebot.v11 import (
    NoticeEvent
)
from typing import Literal

from nonebot.typing import overrides

## todo 不能这样写捏
class GroupCardNoticeEvent(NoticeEvent):
    """群名片修改事件"""

    notice_type: Literal["group_card"]
    user_id: int
    group_id: int
    card_old: str
    card_new: str

    @overrides(NoticeEvent)
    def get_user_id(self) -> str:
        return str(self.user_id)

    @overrides(NoticeEvent)
    def get_session_id(self) -> str:
        return f"group_{self.group_id}_{self.user_id}"