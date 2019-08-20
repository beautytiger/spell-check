from datetime import datetime

now = datetime.now()
begin = "{}-{:02d}-16".format(now.year, now.month-1)
stop = "{}-{:02d}-16".format(now.year, now.month)
begin = datetime.strptime(begin, "%Y-%m-%d")
stop = datetime.strptime(stop, "%Y-%m-%d")
print("begin", begin)
print("stop", stop)

test1 = datetime.strptime("2019-07-15 23:59:59", "%Y-%m-%d %H:%M:%S")
test2 = datetime.strptime("2019-07-16 00:00:00", "%Y-%m-%d %H:%M:%S")

print("test1", test1)
print("test2", test2)

print("test2-test1", test2-test1)
print("test1<begin", test1<begin)
print("test2>begin", test2>begin)
