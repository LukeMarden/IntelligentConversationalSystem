import requests
import json
import datetime
import time
from datetime import datetime, date
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from math import sqrt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.multioutput import MultiOutputRegressor

from sklearn.preprocessing import StandardScaler

import pandas as pd
from pandas import json_normalize
import numpy as np
class prediction():
    def __init__(self, station1, station2, numberOfStops, delayStation, delay, arrivalTime, delayCode=0):
        self.data = self.load_data(station1, station2)
        # self.data = pd.read_pickle('database.pkl')
        self.journey = self.find_journey(numberOfStops, delayStation, delay, delayCode)
        self.predictionModel = self.practical_predict_model()
        self.time = self.predict_journey(arrivalTime, station2)

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
            "to_time": "2359",
            "from_date": "2017-08-01",
            "to_date": "2017-08-03",
            "days": "WEEKDAY"
        }
        rid = []
        r = (requests.post(rids_api_url, headers=headers, auth=auths, json=rids)).json()
        for i in range(len(r['Services'])):
            rid.append(r['Services'][i]['serviceAttributesMetrics']['rids'])
        rid = np.concatenate(np.array(rid, dtype=object))
        data = {}
        time = {}
        database = pd.DataFrame()
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
            df['late_canc_reason'] = df['late_canc_reason'].fillna(value=0)
            df['gbtt_ptd'] = pd.to_datetime(df['gbtt_ptd'], format='%H%M', errors='coerce') - \
                             pd.to_datetime(df['gbtt_ptd'], format='%H%M', errors='coerce').dt.normalize()
            df['gbtt_pta'] = pd.to_datetime(df['gbtt_pta'], format='%H%M', errors='coerce') - \
                             pd.to_datetime(df['gbtt_pta'], format='%H%M', errors='coerce').dt.normalize()
            df['actual_td'] = pd.to_datetime(df['actual_td'], format='%H%M', errors='coerce') - \
                              pd.to_datetime(df['actual_td'], format='%H%M', errors='coerce').dt.normalize()
            df['actual_ta'] = pd.to_datetime(df['actual_ta'], format='%H%M', errors='coerce') - \
                              pd.to_datetime(df['actual_ta'], format='%H%M', errors='coerce').dt.normalize()
            df['arrivalDelay'] = df['actual_ta'].dt.total_seconds()-df['gbtt_pta'].dt.total_seconds()
            df['departureDelay'] = df['actual_td'].dt.total_seconds()- df['gbtt_ptd'].dt.total_seconds()
            df['previousJourney'] = df['gbtt_pta'].dt.total_seconds() - df['gbtt_ptd'].shift().dt.total_seconds()
            df['nextJourney'] = df['gbtt_pta'].shift(-1).dt.total_seconds() - df['gbtt_ptd'].dt.total_seconds()
            df['previousArrivalDelay'] = df['actual_ta'].shift().dt.total_seconds()  - df['gbtt_pta'].shift().dt.total_seconds()
            df['previousDepartureDelay'] = df['actual_td'].shift().dt.total_seconds() - df['gbtt_ptd'].shift().dt.total_seconds()
            df['nextArrivalDelay'] = df['actual_ta'].shift(-1).dt.total_seconds() - df['gbtt_pta'].shift(-1).dt.total_seconds()
            df['nextDepartureDelay'] = df['actual_td'].shift(-1).dt.total_seconds()  - df['gbtt_ptd'].shift(-1).dt.total_seconds()
            df['previousStation'] = df['location'].shift()
            df['nextStation'] = df['location'].shift(-1)
            df['numberOfStops'] = len(df.index)
            database = database.append(df)



        database.to_csv('database.csv')
        database.to_pickle('database.pkl')
        # print(database.loc[[7]])
        return database

    def find_journey(self, numberOfStops, delayStation, delay, delayCode):
        self.journeyData = self.data[self.data['numberOfStops'] == numberOfStops]
        self.journeyData = self.journeyData.drop(columns=['date_of_service', 'toc_code', 'rid',
                                                          'gbtt_ptd', 'gbtt_pta', 'actual_td', 'actual_ta',
                                                          'previousJourney', 'nextJourney'])
        self.journeyData = self.journeyData.drop(columns=['previousStation', 'nextStation'])
        self.journeyData = self.journeyData.head(numberOfStops)
        self.journeyData = self.journeyData.assign(arrivalDelay=0)
        self.journeyData = self.journeyData.assign(departureDelay=0)
        self.journeyData = self.journeyData.assign(previousArrivalDelay=0)
        self.journeyData = self.journeyData.assign(previousDepartureDelay=0)
        self.journeyData = self.journeyData.assign(nextArrivalDelay=0)
        self.journeyData = self.journeyData.assign(nextDepartureDelay=0)
        self.journeyData = self.journeyData.assign(late_canc_reason=delayCode)
        self.journeyData.loc[self.journeyData['location'] == self.find_location_code(delayStation),
                             'departureDelay'] = delay*60

    def accurate_predict_model(self):
        # self.data = pd.get_dummies(self.data, columns=['location'])
        # self.data = pd.get_dummies(self.data, columns=['previousStation'])
        # self.data = pd.get_dummies(self.data, columns=['nextStation'])
        # self.data = pd.get_dummies(self.data, columns=['toc_code'])

        self.data = self.data.drop('rid' ,axis=1)
        self.data['gbtt_ptd'] = self.data['gbtt_ptd'].dt.total_seconds()
        self.data['gbtt_pta'] = self.data['gbtt_pta'].dt.total_seconds()
        self.data['actual_td'] = self.data['actual_td'].dt.total_seconds()
        self.data['actual_ta'] = self.data['actual_ta'].dt.total_seconds()
        self.data['late_canc_reason'] = self.data['late_canc_reason'].fillna(value=0)
        self.data = self.data.drop(columns=['toc_code', 'location', 'nextStation', 'previousStation', 'date_of_service'])
        self.data = self.data.reset_index()
        self.data = self.data.dropna(axis=0)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 15)
        # print(self.data)
        X = self.data.drop(columns=['nextDepartureDelay', 'nextArrivalDelay'])
        Y = self.data[['nextDepartureDelay', 'nextArrivalDelay']]
        scaler = StandardScaler()
        scaler.fit(X)
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.4, random_state=1)
        Xtrain = scaler.transform(Xtrain)
        Xtest = scaler.transform(Xtest)
        mlp = MLPRegressor(hidden_layer_sizes=50,solver='sgd', max_iter=10000, activation='logistic',random_state=0, learning_rate_init=0.001,verbose = 'True',momentum=0.9, tol=0.00002, early_stopping=False)
        mlp.fit(Xtrain, Ytrain)
        Yguess = mlp.predict(Xtest)
        print('RMSE = ', sqrt(mean_squared_error(Ytest, Yguess)), ', R^2 value = ', r2_score(Ytest, Yguess))

        return mlp

    def practical_predict_model(self):
        # self.data = pd.get_dummies(self.data, columns=['location'])

        self.data = self.data.drop('rid', axis=1)
        self.data['gbtt_ptd'] = self.data['gbtt_ptd'].dt.total_seconds()
        self.data['gbtt_pta'] = self.data['gbtt_pta'].dt.total_seconds()
        self.data['actual_td'] = self.data['actual_td'].dt.total_seconds()
        self.data['actual_ta'] = self.data['actual_ta'].dt.total_seconds()
        self.data['late_canc_reason'] = self.data['late_canc_reason'].fillna(value=0)
        self.data = self.data.drop(
            columns=['toc_code', 'location', 'nextStation', 'previousStation', 'date_of_service'])
        self.data = self.data.drop(
            columns=['gbtt_ptd', 'gbtt_pta', 'actual_td', 'actual_ta', 'nextJourney', 'previousJourney', 'numberOfStops'])
        self.data = self.data.reset_index()
        self.data = self.data.dropna(axis=0)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 15)
        # print(self.data)
        X = self.data.drop(columns=['nextDepartureDelay', 'nextArrivalDelay'])
        Y = self.data[['nextDepartureDelay', 'nextArrivalDelay']]
        scaler = StandardScaler()
        scaler.fit(X)
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.4, random_state=1)
        Xtrain = scaler.transform(Xtrain)
        Xtest = scaler.transform(Xtest)
        mlp = MLPRegressor(hidden_layer_sizes=50, solver='sgd', max_iter=10000, activation='logistic', random_state=0,
                           learning_rate_init=0.001, verbose='True', momentum=0.9, tol=0.00002, early_stopping=False)
        mlp.fit(Xtrain, Ytrain)
        Yguess = mlp.predict(Xtest)
        print('RMSE = ', sqrt(mean_squared_error(Ytest, Yguess)), ', R^2 value = ', r2_score(Ytest, Yguess))

        return mlp

    def predict_journey(self, arrivalTime, station2):
        self.predictData = self.journeyData[(self.journeyData['departureDelay'] > 0).idxmax():]
        # self.predictData = pd.get_dummies(self.predictData, columns=['location'])
        X = self.predictData.drop(columns=['location', 'nextDepartureDelay', 'nextArrivalDelay'])
        Y = pd.DataFrame()
        for index in range(len(self.predictData.index)):
            if index+1 < len(self.predictData.index):
                Y = Y.append(pd.DataFrame(self.predictionModel.predict(X.iloc[[index]])))
                X['arrivalDelay'].iloc[[index+1]] = Y[0].iloc[[index]]
                X['departureDelay'].iloc[[index + 1]] = Y[1].iloc[[index]]
            if index > 0:
                X['previousArrivalDelay'].iloc[[index]] = X['arrivalDelay'].iloc[[index-1]]
                X['previousDepartureDelay'].iloc[[index]] = X['departureDelay'].iloc[[index-1]]
        X = X.reset_index()
        Y = Y.reset_index()
        Z = (pd.concat([X, Y], axis=1)).drop(columns='index')
        # print(Z)
        rowsRemoved = len(self.journeyData.index) - len(self.predictData.index)
        index = (self.journeyData[self.journeyData['location'] ==
                                  self.find_location_code(station2)].index.values - rowsRemoved)[0]

        date = datetime.strptime(str(arrivalTime), '%H%M').time()
        totalSeconds = ((date.hour * 60 + date.minute) * 60 + date.second) + Z['arrivalDelay'].iloc[index]
        predictedArrivalTime = time.strftime('%H:%M:%S', time.gmtime(totalSeconds))
        Z.to_csv('Z.csv')
        print(predictedArrivalTime)
        return predictedArrivalTime


