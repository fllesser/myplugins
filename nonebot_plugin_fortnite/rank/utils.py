from utils.image_utils import BuildMat
from configs.path_config import IMAGE_PATH
from typing import List, Union
import os

def _init_rank_graph(
    title: str, _uname_lst: List[str], _num_lst: List[Union[int, float]]
) -> BuildMat:
    """
    生成排行榜统计图
    :param title: 排行榜标题
    :param _uname_lst: 用户名列表
    :param _num_lst: 数值列表
    """
    image = BuildMat(
        y=_num_lst,
        y_name="* 可以在命令后添加数字来指定排行人数 至多 50 *",
        mat_type="barh",
        title=title,
        x_index=_uname_lst,
        display_num=True,
        x_rotate=30,
        background=[
            f"{IMAGE_PATH}/background/create_mat/{x}"
            for x in os.listdir(f"{IMAGE_PATH}/background/create_mat")
        ],
        font_size= int(22 * (1 - len(_uname_lst) / 100)),
        bar_color=["*"],
    )
    image.size = (1200, 1000)
    image.gen_graph()
    return image