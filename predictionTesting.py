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
headers = { "Content-Type": "application/json" }
auths = ('lmarden7@gmail.com', 'Qwer1234@')
# train_data = pd.read_csv('TrainData/a51/NRCH_LIVST_OD_a51_2017_1_1.csv')
# train_data = train_data[train_data.wtp.isnull()]
# X = train_data.iloc[:, [3,18,20]]
# Y = train_data.iloc[:, 16]
# print(Y)
# X.dep_at =  pd.to_datetime(X.dep_at, format='%H:%M')
# X.ptd =  pd.to_datetime(X.ptd, format='%H:%M')
#
# print(X.dep_at - X.ptd)
# print(X.dep_at - X.)


# scaler = StandardScaler()
# scaler.fit(X)
#
# Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.5, random_state=1)
#
# Xtrain = scaler.transform(Xtrain)
# Xtest = scaler.transform(Xtest)
#
#
# mlp = MLPRegressor(hidden_layer_sizes=20,solver='sgd', max_iter=10000, activation='logistic',random_state=0, learning_rate_init=0.001,verbose = 'True',momentum=0.9, tol=0.0001, early_stopping=False)
# mlp.fit(Xtrain, Ytrain)
#
# Yguess = mlp.predict(Xtest)
# sqrt(mean_squared_error(Ytest, Yguess)), r2_score(Ytest, Yguess)
time_api_url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
rid = "201701057101328"
time = {}
data = {}
time[rid] = {
    "rid": "201707287101237"
}
p = requests.post(time_api_url, headers=headers, auth=auths, json=time[rid])
data[rid] = (json.loads(p.text))['serviceAttributesDetails']
df = pd.DataFrame(columns=['date','rid','toc','previousStation','currentStation','nextStation','departureDelay',
                           'arrivalDelay','previousTravelTime','nextTravelTime','previousDepartureDelay','delayReason',
                           'nextArrivalDelay'])


data[rid]['date_of_service'] = datetime.datetime.strptime(data[rid]['date_of_service'], "%Y-%m-%d")
data[rid]['rid'] = int(data[rid]['rid'])
for i in range(len(data[rid]['locations'])):

    data[rid]['locations'][i]['gbtt_ptd'] = pd.to_datetime(data[rid]['locations'][i]['gbtt_ptd'], format='%H%M', errors='coerce')
    data[rid]['locations'][i]['gbtt_pta'] = pd.to_datetime(data[rid]['locations'][i]['gbtt_pta'], format='%H%M', errors='coerce')
    data[rid]['locations'][i]['actual_td'] = pd.to_datetime(data[rid]['locations'][i]['actual_td'], format='%H%M', errors='coerce')
    data[rid]['locations'][i]['actual_ta'] = pd.to_datetime(data[rid]['locations'][i]['actual_ta'], format='%H%M', errors='coerce')
    data[rid]['locations'][i]['late_canc_reason'] = \
        int(data[rid]['locations'][i]['late_canc_reason']) if data[rid]['locations'][i]['late_canc_reason'] else 0

df = pd.DataFrame.from_dict(data[rid], orient='columns')
df = pd.concat([pd.DataFrame(data[rid]),
                json_normalize(data[rid]['locations'])],
               axis=1).drop('locations', 1)
df['departureDelay'] = (df['actual_td'] - df['gbtt_ptd']).dt.seconds / 60
df['arrivalDelay'] = (df['actual_ta'] - df['gbtt_pta']).dt.seconds / 60
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

print(df.dtypes)
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 18)
print(df)
# print(data[rid]['locations'][[0,1,2]]['location'])