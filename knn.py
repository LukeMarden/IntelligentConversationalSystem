import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn import neighbors
import pandas as pd

train_data = pd.read_csv('TrainData/a51/NRCH_LIVST_OD_a51_2017_1_1.csv')
train_data = train_data[train_data.wtp.isnull()]
print(train_data.head(10))
y = train_data.iloc[:,16]
X = train_data.iloc[:,[3,18,20]]

def f(x): #define a linear function
    return (2*x + 5).ravel()
np.random.seed(1) # set a seed for random number generator
# generate training data X
# X = np.linspace(0, 80, 40)[:, np.newaxis]
# y = f(X) + 20*(0.5-np.random.rand(40).ravel())
T = np.linspace(0,80,100)[:,np.newaxis] #generate test data
# create a kNN model without weighting on data
knn_u = neighbors.KNeighborsRegressor(3, weights='uniform')
knn = knn_u.fit(X, y)
y_knn = knn.predict(T)
plt.scatter(X, y, color='black', label='training data')
plt.plot(T, y_knn, color = 'g', label = 'knn_u')
plt.show()