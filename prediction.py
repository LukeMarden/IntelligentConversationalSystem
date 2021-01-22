import requests
import json
import datetime
import pandas as pd
from pandas import json_normalize
import numpy as np
class prediction():
    def __init__(self):
        self.data = self.load_data()

    def find_location_code(self, station):
        stations = json.load(open('train_codes.json', 'r'))
        return stations[station]

    def load_data(self):
        headers = { "Content-Type": "application/json" }
        auths = ('lmarden7@gmail.com', 'Qwer1234@')
        rids_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
        time_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
        rids = {
            "from_loc": "NRW",
            "to_loc": "LST",
            "from_time": "0000",
            "to_time": "1159",
            "from_date": "2017-07-01",
            "to_date": "2017-08-01",
            "days": "WEEKDAY"
        }
        rid = []
        r = (requests.post(rids_api_url, headers=headers, auth=auths, json=rids)).json()
        for i in range(len(r['Services'])):
            # print(r['Services'][i]['serviceAttributesMetrics']['rids'])
            rid.append(r['Services'][i]['serviceAttributesMetrics']['rids'])
        rid = (np.array(rid)).ravel()
        # print(rid)
        # print(rid)
        data = {}
        time = {}
        # datebase = pd.DataFrame(columns=['date','rid','toc','previousStation','currentStation','nextStation','departureDelay',
        #                            'arrivalDelay','previousTravelTime','nextTravelTime','previousDepartureDelay','delayReason',
        #                            'nextArrivalDelay'])
        datebase = pd.DataFrame()
        # for j in range(len(rid)):
        for j in range(1):
            time[rid[j]] = {
                # "rid": rid[j]
                'rid': '201707287101237'
            }

            p = requests.post(time_api_url, headers=headers, auth=auths, json=time[rid[j]])
            data[rid[j]] = (json.loads(p.text))['serviceAttributesDetails']
            data[rid[j]]['date_of_service'] = datetime.datetime.strptime(data[rid[j]]['date_of_service'], "%Y-%m-%d")
            data[rid[j]]['rid'] = int(data[rid[j]]['rid'])
            for i in range(len(data[rid[j]]['locations'])):
                data[rid[j]]['locations'][i]['gbtt_ptd'] = pd.to_datetime(data[rid[j]]['locations'][i]['gbtt_ptd'], format='%H%M', errors='coerce')
                data[rid[j]]['locations'][i]['gbtt_pta'] = pd.to_datetime(data[rid[j]]['locations'][i]['gbtt_pta'], format='%H%M', errors='coerce')
                data[rid[j]]['locations'][i]['actual_td'] = pd.to_datetime(data[rid[j]]['locations'][i]['actual_td'], format='%H%M', errors='coerce')
                data[rid[j]]['locations'][i]['actual_ta'] = pd.to_datetime(data[rid[j]]['locations'][i]['actual_ta'], format='%H%M', errors='coerce')
                data[rid[j]]['locations'][i]['late_canc_reason'] = \
                    int(data[rid[j]]['locations'][i]['late_canc_reason']) if data[rid[j]]['locations'][i]['late_canc_reason'] else 0

            df = pd.DataFrame.from_dict(data[rid[j]], orient='columns')
            df = pd.concat([pd.DataFrame(data[rid[j]]),
                            json_normalize(data[rid[j]]['locations'])],
                           axis=1).drop('locations', 1)
            df['arrivalDelay'] = (df['actual_ta'] - df['gbtt_pta']).dt.seconds / 60
            # Is currently subtracting year as well so doensnt work for negative delays
            df['previousJourney'] = (df['gbtt_pta'] - df['gbtt_ptd'].shift()).dt.seconds/60
            df['nextJourney'] = (df['gbtt_pta'].shift(-1) - df['gbtt_ptd']).dt.seconds/60
            df['previousDepartureDelay'] = (df['actual_td'].shift() - df['gbtt_ptd'].shift()).dt.seconds / 60
            df['nextArrivalDelay'] = (df['actual_ta'].shift(-1) - df['gbtt_pta'].shift(-1)).dt.seconds / 60
            df['gbtt_ptd'] = df['gbtt_ptd'].dt.time
            df['gbtt_pta'] = df['gbtt_pta'].dt.time
            df['actual_td'] = df['actual_td'].dt.time
            df['actual_ta'] = df['actual_ta'].dt.time
            df['previousStation'] = df['location'].shift()
            df['nextStation'] = df['location'].shift(-1)

            datebase = datebase.append(df)

        pd.set_option('display.max_rows', 16)
        pd.set_option('display.max_columns', 120)
        # print(datebase)
        print(datebase.dtypes)
        datebase.to_csv('database.csv')

# rids_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
# rids = {
#     "from_loc": "NRW",
#     "to_loc": "LST",
#     "from_time": "0000",
#     "to_33.33.3.3.                                                                                                                                                                                                             time": 1"2359",
#     "from_date": "2016-07-01",
#     "to_date": "2016-12-31",
#     "days": "WEEKDAY"
# }
# r = requests.post(rids_api_url, headers=headers, auth=auths, json=rids)
# print(json.dumps(json.loads(r.text), sort_keys=True, indent=2, separators=(',',': ')))