import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as md
# date = datetime.now().strftime("%Y-%m-%d")
import json
def get_rate(date):


    r = requests.get("http://api.fixer.io/" + date.strftime("%Y-%m-%d"), {"base":"GBP"})


    return r.json()["rates"]

start = datetime(2016,01,06)
end = datetime(2016,06,30)
date = start

rate = []
dates = []
while date <= end:

    dates.append(date)
    rate.append(get_rate(date))
    date += timedelta(days=1)


json.dump({"usd-gbp":rate,"dates":dates}, open("gbp-usd.json","w"), default=lambda obj: (obj.isoformat() if isinstance(
    obj,
                                                                                                  datetime) else None))

gdb_usd = [i["USD"] for i in rate]
xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
_,ax = plt.subplots()
ax.plot(dates,gdb_usd)
ax.xaxis.set_major_formatter(xfmt)
plt.show()