import re
sql = '\d dsfhsjkladjf; lksdjflkasdj flksdjfl;asdkjf klsdjflsdakfj ls;dkfj lsdkfj slkjdf lksdjf lkssdf sdfsdfsda fsda fsdfasdf'
if re.search('select', sql, flags=0) or re.search(r'\\d', sql, flags=0):
    print(sql[0:100])
    print("hello")