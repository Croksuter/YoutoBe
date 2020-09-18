from pendulum.parsing import parse_iso8601
import datetime
data = parse_iso8601('PT04M19S')
d,h,m,s = data.days, data.hours, data.minutes, data.seconds
if d != 0:
    timestamp = "{:02}:".format(d) + datetime.datetime(2000,10,1,hour=h, minute=m, second=s).strftime('%H:%M:%S')
else:
    timestamp = datetime.datetime(2000, 10, 1, hour=h, minute=m, second=s).strftime('%H:%M:%S')
print(str(timestamp))