import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn import tree
import time
import matplotlib.pyplot as plt


def calc(path, percent):
    data = pd.read_csv(path)
    features = ["latitude", "longitude", "depth", ]
    X = data[features]
    y = data["mag"]
    percent = percent/100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=percent, random_state=42)

    # Train a random forest regression model
    neigh = KNeighborsRegressor(n_neighbors=3)
    neigh.fit(X_train, y_train)

    # Make predictions on the test set
    # X_test.loc[:, "time"] = pd.to_datetime(X_test["time"]).apply(lambda x: int(time.mktime(x.timetuple())))
    y_pred = neigh.predict(X_test)

    # Evaluate the model's performance

    mse = mean_squared_error(y_test, y_pred)
    return mse, y_pred, neigh

def data_plot(plot_type,path):
    data = pd.read_csv(path)
    if plot_type == 'Магнитуда':
        return data['mag']
    elif plot_type == 'Глубина':
        return data['depth']
    else:
        return 'None'


def pred(lat,long,depth,neigh):
    res = neigh.predict([[lat,long,depth]])
    return res
"""
X = data.loc[:, ['latitude', 'longitude', 'depth']].values
y = data['mag']

neigh = KNeighborsRegressor(n_neighbors=3)
neigh.fit(X_train, y_train)
print(neigh.predict([[42.3331,144.5555,47.631]]))
#print(neigh.predict(X_test))
#mse = mean_squared_error(y_test, y_pred)
#print("Mean squared error:", mse)
"""