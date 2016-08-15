import requests
import datetime
import time
import logging


class GuardianWrapper(object):
    _logger = logging.getLogger(__name__)
    BASE_URL = "http://content.guardianapis.com/search"

    def __init__(self, api_key):
        self.api_key = api_key
        self.time_of_last_request = None

    def query_topics(self, topic_list, start_date=None, end_date=None):

        result = self.query(" AND ".join(topic_list), start_date, end_date)
        # print topic_list
        # print result
        if len(result) > 0:
            return result
        else:

            self._logger.info("Could not find any results using AND switching to OR")
            results = self.query(" OR ".join(topic_list), start_date, end_date)
            # print results
            return results

    def query(self, topics, start_date=None, end_date=None):

        params = {"q": topics, "api-key": self.api_key, "tag":"politics/eu-referendum"}

        if self.time_of_last_request is not None:
            time_since = (datetime.datetime.now() - self.time_of_last_request).total_seconds()
            if time_since < 1.0:
                self._logger.info("Waiting as more too many requests to Guardian API %d s", time_since)
                time.sleep(abs(1.0 - time_since))

        if start_date is not None:
            params["from-date"] = start_date.isoformat()
        if end_date is not None:
            params["to-date"] = end_date.isoformat()
        # if start_date is not None or end_date is not None:
        #     params["use-date"] = "published"

        response = requests.get(self.BASE_URL, params)
        self.time_of_last_request = datetime.datetime.now()
        response_json = response.json()["response"]

        if response_json["status"] != "ok":
            return []
        else:
            return [i["webTitle"] for i in response_json["results"]]


if __name__ == "__main__":
    wrapper = GuardianWrapper("4d547cbd-99e2-4b00-a40e-987c67c252b8")
    print wrapper.query_topics([u'EU',u'Cameron', u'PM', u'immigration', u'Turkey', u'UK'],
                               datetime.datetime(2016, 06, 19, 17),
                               datetime.datetime(2016, 06, 19, 23, 59))
