import requests
topic = "eu referendum"
key = "4d547cbd-99e2-4b00-a40e-987c67c252b8"
from_date = "2016-02-19"
to_date ="2016-02-21"
url = "http://content.guardianapis.com/search?q=" + topic + "&" + "from-date=" + from_date + "&" + \
      "to-date=" + \
      to_date \
      + "&use-date=published&api-key=" + key
import json
import pprint
a = requests.get(url)
b = a.json()
pprint.pprint([i["webTitle"] for i in b["response"]["results"]])





