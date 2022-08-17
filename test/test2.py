

members = []
# 当前时间戳

for i in range(1, 20):
    try:
        print(f"第{i}次查询条数, 已匹配的待踢人数{len(members)}")
    except:
        print("异常")
