import time

import requests
from pymongo import MongoClient

from AnalysisEngine.TwitterObj import Status

api_key = "AIzaSyDigmTpI9nc7y7qTt7WheHBesBfEM_kh8E"
timestamp = time.time()
# api_response = requests.get('https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&key={3}'.format(latitude,longitude,timestamp,api_key))
# api_response_dict = api_response.json()
# print api_response_dict
# if api_response_dict['status'] == 'OK':
#     print api_response_dict


key = "RSWI54WQ9VSF"

last_call = time.time()
def get_time_zone(longitude,latitude):
    time.sleep(1)


    api_response = requests.get("http://api.timezonedb.com/v2/get-time-zone?"
                                "key={0}&"
                                "by=position&"
                                "lat={1}&"
                                "lng={2}&"
                                "format=json".format(key, latitude, longitude))
    if api_response.status_code != 200:
        print "ERRRRRROOOORRRRR"
        print api_response.status_code
        return None
    api_response_dict = api_response.json()
    if api_response_dict['status'] == 'OK':
        return api_response_dict


# def get_time_zone_google(longitude,latitude):
#     api_response = requests.get('https://maps.googleapis.com/maps/api/timezone/json?location={0},{1}&timestamp={2}&key={3}'.format(latitude,longitude,timestamp,api_key))
#     api_response_dict = api_response.json()
#     return api_response_dict



db_col = MongoClient().get_database("DATA").get_collection("Brexit_old")
cursor = db_col.find({"user.utcOffset":{"$nin": [None, -1]},
                      "geoLocation":{"$ne":None, "$exists":True}})
print "Getting list"
l = list(cursor)
print "got list"
# print cursor.count()
wrong = 0
total = 0
import csv
with open("out.csv","w'") as f:
    writer = csv.writer(f, delimiter=',')
    for c in l:
        s = Status(c, "T4J")

        utc_offset = float(s.get_user().get_utc_offset()) / (60*60)

        lat = s.get_coordinates().get_latitude()
        lng = s.get_coordinates().get_longitude()
        result = get_time_zone(lng,lat)
        if result is None:
            print "Continueing"
            continue
        found_offset = float(result["gmtOffset"]) / (60 * 60)
        if found_offset != utc_offset:
            wrong +=1
            print "!!",
        total +=1
        print "Twitter UTC offset = {0}," \
              "Found Offset = {1}," \
              "Coordinates({2},{3})," \
              "Country = {4}".format(utc_offset,found_offset,lng,lat,result["countryName"]), total
        # print result
        writer.writerow([utc_offset,found_offset,lng,lat,result["countryName"]])
        if divmod(total,10)[1] == 0:
            f.flush()

print wrong, total


latitude  = 51.4870029
longitude = -0.1689445
