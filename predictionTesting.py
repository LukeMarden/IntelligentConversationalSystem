import requests
import json
import pandas as pd

# train_data = pd.read_csv('TrainData/a51/NRCH_LIVST_OD_a51_2017_1_1.csv')
# print(train_data.head(10))
# Y = train_data.iloc[:,16]
# print(Y)
# X = train_data.iloc[:,[3,18,20]]
# print(X)



headers = { "Content-Type": "application/json" }
auths = ('lmarden7@gmail.com', 'Qwer1234@')
rids_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
rids = {
    "from_loc": "NRW",
    "to_loc": "LST",
    "from_time": "0000",
    "to_time": "2359",
    "from_date": "2016-07-01",
    "to_date": "2017-12-31",
    "days": "WEEKDAY"
}
r = requests.post(rids_api_url, headers=headers, auth=auths, json=rids)
print(json.dumps(json.loads(r.text), sort_keys=True, indent=2, separators=(',',': ')))
#
# time_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
# rid = "201701057101328"
# time = {}
# data = {}
# time[rid] = {
#     "rid": "201701057101328"
# }
# p = requests.post(time_api_url, headers=headers, auth=auths, json=time[rid])
# data[rid] = (json.loads(p.text))['serviceAttributesDetails']
# # stuff = data['serviceAttributesDetails']['locations'][10]['location']
# print(data[rid])
# for i in range(len(data[rid])):
#     print(data[rid][i]['location'])


