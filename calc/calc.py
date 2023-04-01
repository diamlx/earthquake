import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn import tree
import time

def calc(path):
    data = pd.read_csv(path)
    features = ["latitude", "longitude", "depth", ]
    X = data[features]
    y = data["mag"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a random forest regression model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Make predictions on the test set
    # X_test.loc[:, "time"] = pd.to_datetime(X_test["time"]).apply(lambda x: int(time.mktime(x.timetuple())))
    y_pred = rf.predict(X_test)

    # Evaluate the model's performance
    print(X_test)
    print(y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean squared error:", mse)

