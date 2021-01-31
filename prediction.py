import requests
import json
import datetime
from datetime import datetime, date
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.feature_extraction import DictVectorizer
from math import sqrt

from sklearn.preprocessing import StandardScaler

import pandas as pd
from pandas import json_normalize
import numpy as np
class prediction():
    def __init__(self, station1, station2):
        # self.data = self.load_data(station1, station2)
        self.data = pd.read_pickle('database.pkl')
        self.plot = self.plot_data()

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
        rid = np.concatenate(np.array(rid, dtype=object))
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

        datebase.to_pickle('database.pkl')

    def plot_data(self):
        self.data = pd.get_dummies(self.data, columns=['location'])
        self.data = pd.get_dummies(self.data, columns=['previousStation'])
        self.data = pd.get_dummies(self.data, columns=['nextStation'])
        self.data = pd.get_dummies(self.data, columns=['toc_code'])
        self.data = self.data.drop('date_of_service' ,axis=1)
        self.data = self.data.drop('rid' ,axis=1)
        self.data['gbtt_ptd'] = self.data['gbtt_ptd'].dt.total_seconds()
        self.data['gbtt_pta'] = self.data['gbtt_pta'].dt.total_seconds()
        self.data['actual_td'] = self.data['actual_td'].dt.total_seconds()
        self.data['actual_ta'] = self.data['actual_ta'].dt.total_seconds()
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 15)
        # print(self.data)
        X = self.data.loc[:, self.data.columns != 'nextArrivalDelay']
        Y = self.data.iloc[:, 10]
        print(X)
        print(Y)
        # vectorizer = DictVectorizer()
        # vector_data = vectorizer.fit_transform(X)
        # scaler = StandardScaler()
        # scaler.fit(X)
        # Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.5, random_state=1)
        # Xtrain = scaler.transform(Xtrain)
        # Xtest = scaler.transform(Xtest)
        # mlp = MLPRegressor(hidden_layer_sizes=20,solver='sgd', max_iter=10000, activation='logistic',random_state=0, learning_rate_init=0.001,verbose = 'True',momentum=0.9, tol=0.0001, early_stopping=False)
        # mlp.fit(Xtrain, Ytrain)
        # Yguess = mlp.predict(Xtest)
        # sqrt(mean_squared_error(Ytest, Yguess)), r2_score(Ytest, Yguess)


