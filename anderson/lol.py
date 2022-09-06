from nonebot.plugin import on_command

lol = on_command("lolzh", block=True)

@lol.handle()
async def _():
    lollist = {"2412125282" : "gocqhttp11",
                "501273515" : "202nhkgo",
                "3248891254" : "xxgg0314",
                "3147682968" : "1942422015194cpy",
                "3448546405" : "1942422015194cpy"}
    msg = ""
    for i in lollist:
        msg += f"{i}\t{lollist[i]}\n"
    await lol.finish(message=msg)

