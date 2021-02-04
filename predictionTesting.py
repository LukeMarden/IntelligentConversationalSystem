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
rids_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
time_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
timetable_api_url = "https://opendata.nationalrail.co.uk/api/staticfeeds/3.0/timetable"
token_api_url = "https://opendata.nationalrail.co.uk/authenticate"
rids = {

    'username':'lmarden7@gmail.com',
    'password':'Qwer1234@'

}

rid = []
r = ((requests.post(token_api_url, headers=headers, json=rids)).json())['token']
print(r)
auths = {"X-Auth-Token":r}
timetable = {
    'token':r
}

timetable1 = (requests.post(timetable_api_url, headers=headers, auth=auths, json=timetable)).json()
print(timetable1)