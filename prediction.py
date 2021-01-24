import requests
import json
import datetime
from datetime import datetime, date

import pandas as pd
from pandas import json_normalize
import numpy as np
class prediction():
    def __init__(self, station1, station2):
        self.data = self.load_data(station1, station2)

    def find_location_code(self, station):
        stations = json.load(open('train_codes.json', 'r'))
        return stations[station]

    def load_data(self, station1, station2):
        headers = { "Content-Type": "application/json" }
        auths = ('lmarden7@gmail.com', 'Qwer1234@')
        rids_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
        time_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
        rids = {
            "from_loc": self.find_location_code(station1),
            "to_loc": self.find_location_code(station2),
            "from_time": "0000",
            "to_time": "1159",
            "from_date": "2017-07-01",
            "to_date": "2017-08-01",
            "days": "WEEKDAY"
        }
        rid = []
        r = (requests.post(rids_api_url, headers=headers, auth=auths, json=rids)).json()
        for i in range(len(r['Services'])):
            rid.append(r['Services'][i]['serviceAttributesMetrics']['rids'])
        rid = (np.array(rid)).ravel()
        data = {}
        time = {}
        datebase = pd.DataFrame()
        for j in range(len(rid)):
            time[rid[j]] = {
                "rid": rid[j]
            }

            p = requests.post(time_api_url, headers=headers, auth=auths, json=time[rid[j]])
            data[rid[j]] = (json.loads(p.text))['serviceAttributesDetails']
            data[rid[j]]['date_of_service'] = datetime.strptime(data[rid[j]]['date_of_service'], "%Y-%m-%d")
            data[rid[j]]['rid'] = int(data[rid[j]]['rid'])
            for i in range(len(data[rid[j]]['locations'])):
                data[rid[j]]['locations'][i]['late_canc_reason'] = \
                    int(data[rid[j]]['locations'][i]['late_canc_reason']) if data[rid[j]]['locations'][i]['late_canc_reason'] else 0

            df = pd.DataFrame.from_dict(data[rid[j]], orient='columns')
            df = pd.concat([pd.DataFrame(data[rid[j]]),
                            json_normalize(data[rid[j]]['locations'])],
                           axis=1).drop('locations', 1)
            df['gbtt_ptd'] = pd.to_datetime(df['gbtt_ptd'], format='%H%M', errors='coerce') - \
                             pd.to_datetime(df['gbtt_ptd'], format='%H%M', errors='coerce').dt.normalize()
            df['gbtt_pta'] = pd.to_datetime(df['gbtt_pta'], format='%H%M', errors='coerce') - \
                             pd.to_datetime(df['gbtt_pta'], format='%H%M', errors='coerce').dt.normalize()
            df['actual_td'] = pd.to_datetime(df['actual_td'], format='%H%M', errors='coerce') - \
                              pd.to_datetime(df['actual_td'], format='%H%M', errors='coerce').dt.normalize()
            df['actual_ta'] = pd.to_datetime(df['actual_ta'], format='%H%M', errors='coerce') - \
                              pd.to_datetime(df['actual_ta'], format='%H%M', errors='coerce').dt.normalize()
            df['arrivalDelay'] = df['actual_ta'].dt.total_seconds()/60-df['gbtt_pta'].dt.total_seconds()/60
            df['departureDelay'] = df['actual_td'].dt.total_seconds()/60 - df['gbtt_ptd'].dt.total_seconds()/60
            df['previousJourney'] = df['gbtt_pta'].dt.total_seconds()/60 - df['gbtt_ptd'].shift().dt.total_seconds()/60
            df['nextJourney'] = df['gbtt_pta'].shift(-1).dt.total_seconds()/60 - df['gbtt_ptd'].dt.total_seconds()/60
            df['previousDepartureDelay'] = df['actual_td'].shift().dt.total_seconds()/60 - df['gbtt_ptd'].shift().dt.total_seconds()/60
            df['nextArrivalDelay'] = df['actual_ta'].shift(-1).dt.total_seconds()/60 - df['gbtt_pta'].shift(-1).dt.total_seconds()/60
            df['previousStation'] = df['location'].shift()
            df['nextStation'] = df['location'].shift(-1)
            datebase = datebase.append(df)

        datebase.to_csv('database.csv')
