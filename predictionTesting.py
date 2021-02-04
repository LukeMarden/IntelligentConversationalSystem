import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from math import sqrt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn import neighbors
from datetime import datetime, date
import datetime
import pandas as pd
from pandas import json_normalize
import requests
import json
import datetime
from datetime import datetime, date

import pandas as pd
from pandas import json_normalize
import numpy as np
headers = { "Content-Type": "application/json" }
auths = ('lmarden7@gmail.com', 'Qwer1234@')
rids_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
time_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
rids = {
    "from_loc": 'NRW',
    "to_loc": 'LST',
    "from_time": "1200",
    "to_time": "1657",
    "from_date": "2021-02-02",
    "to_date": "2021-02-02",
    "days": "WEEKDAY"
}
rid = []
r = (requests.post(rids_api_url, headers=headers, auth=auths, json=rids)).json()
print(r)
# for i in range(len(r['Services'])):
#     print(r['Services'][i]['serviceAttributesMetrics']['rids'])
#     rid.append(r['Services'][i]['serviceAttributesMetrics']['rids'])
# rid = np.concatenate(np.array(rid))
# data = {}
# time = {}
# datebase = pd.DataFrame()

print(rid)
for j in range(len(rid)):
    # print(rid[j])
    time[rid[j]] = {
        "rid": rid[j]
    }

    p = requests.post(time_api_url, headers=headers, auth=auths, json=time[rid[j]])
    data[rid[j]] = (json.loads(p.text))['serviceAttributesDetails']
    data[rid[j]]['date_of_service'] = datetime.strptime(data[rid[j]]['date_of_service'], "%Y-%m-%d")
    data[rid[j]]['rid'] = int(data[rid[j]]['rid'])
    df = pd.DataFrame.from_dict(data[rid[j]], orient='columns')
    df = pd.concat([pd.DataFrame(data[rid[j]]),
                    json_normalize(data[rid[j]]['locations'])],
                   axis=1).drop('locations', 1)
    df['late_canc_reason'] = pd.to_numeric(df['late_canc_reason'], errors='coerce')
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