class MyStr():

    value: str = ''

    def appendLine(self, s: str) -> 'MyStr':
        self.value += s + "\n"
        return self

    def append(self, s: str) -> str:
        return self.value + s


# print(MyStr()
#         .appendLine("测试换行")
#         .appendLine("测试换行")
#         .append("测试"))