import json

from adminka.source.Logging import Logging


class Location:
    def __init__(self):
        self._log = Logging('logs/main.log')

    def get_current_loc(self, timeout):
        data = {"lat": "55.7558", "lon": "37.6176"}
        self._log.write_log("GET_CUR_LOCATION", "SUCCESSFULL, timeout {}".format(timeout))
        return json.dumps(data)

    def get_loc_bssid(self, bssid):
        data = {"lat": "56.7558", "lon": "36.6176"}
        self._log.write_log("GET_BSSID_LOCATION", "SUCCESSFULL, BSSID {}".format(bssid))
        return json.dumps(data)

    def get_loc_essid(self, essid):
        data = {"lat": "54.7558", "lon": "38.6176"}
        self._log.write_log("GET_ESSID_LOCATION", "SUCCESSFULL, ESSID {}".format(essid))
        return json.dumps(data)

loc = Location()
print(loc.get_current_loc(5))
print(loc.get_loc_bssid('AAA'))
print(loc.get_loc_essid('BBB'))
