member_list = { 12391284 : "haha" , 1231283 : "sdfasdf" }
member_list[123123] = "dsfasdf"
for i in member_list:
    print(type(i))
print(f"{', '.join((str(k) + '->' + v ) for k, v in member_list.items())}")

#12 34 56
