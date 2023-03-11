# 适用于zhenxun_bot的插件
- nonebot_plugin_abstract : 抽象化语句 插件作者仓库[地址](https://github.com/CherryCherries/nonebot-plugin-abstract)
- nonebot_plugin_auto_nickname : qq群时间昵称
- nonebot_plugin_gm_manager : 群成员管理 (踢/禁 自动踢不活跃用户)
- nonebot_plugin_petpet : 头像表情包 插件作者仓库[地址](https://github.com/noneplugin/nonebot-plugin-petpet)
- nonebot_plugin_tsc : 今日校园自动签到(支持随机时间)
- nonebot_plugin_todo : 代办提醒(很抽象)
- nonebot_plugin_merge_group : 合并群聊(未开源)

- nonebot_plugin_fortnite: 堡垒之夜插件整合
  - pve_vb 每日vb图
  - rank 战绩查询
  - daily_shop  每日商城


# 使用说明
 1. 先成功安装并运行[zhenxun_bot](https://github.com/HibiKier/zhenxun_bot)
 2. cd到zhenxun目录, git clone 这个仓库, 将文件夹重命名为 myplugins (根据自己喜好)
 3. bot.py文件中添加一行`nonebot.load_plugins("myplugins")`重启zhenxun_bot, 不需要的插件自行删除