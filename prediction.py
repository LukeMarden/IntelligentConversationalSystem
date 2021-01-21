import requests
import json
class prediction():
    def __init__(self):
        print()




headers = { "Content-Type": "application/json" }
auths = ('lmarden7@gmail.com', 'Qwer1234@')
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





time_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
rid = "201701057101328"
time = {}
data = {}
time[rid] = {
    "rid": "201701057101328"
}
p = requests.post(time_api_url, headers=headers, auth=auths, json=time[rid])
data[rid] = (json.loads(p.text))['serviceAttributesDetails']
print(data[rid])
for i in range(len(data[rid]['locations'])):
    print(data[rid]['locations'][i])