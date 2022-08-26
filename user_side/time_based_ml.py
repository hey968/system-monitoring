from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import plotly.express as px
import joblib
import json
import os


def train_ml_for_user(user):
    with open("configure.json", "r") as fd:
        json_data = json.load(fd)
    pwd = json_data["user_side_loc"]

    df = pd.read_csv(pwd+user+"_time_based_test.csv")
    word_df = df[["command", "time_to_write", "time_in_day"]]
    word_df["hour"] = word_df.time_in_day.apply(lambda x: int(x.split(":")[0]))
    word_df["minute"] = word_df.time_in_day.apply(lambda x: int(x.split(":")[1]))
    word_df = word_df.sort_values(by=['hour', 'minute'])
    X = word_df.iloc[:,[1,3,4]].values

    #print(X)
    # sc = StandardScaler()
    # X = sc.fit_transform(X)
    clf = IsolationForest(random_state=42,contamination=0.1)
    y_pred = clf.fit_predict(X)

    # print(clf.predict(sc.transform(np.array([0.222, '17', '50']).reshape(1, 3))))
    #
    # print(clf.predict(sc.transform(np.array([0.215, '7', '54']).reshape(1, 3))))
    # print(clf.predict(sc.transform(np.array([0.8, '4', '54']).reshape(1, 3))))
    #joblib.dump(clf,pwd+user+"_isloated_forest.pkl")
    #joblib.dump(sc,"std_scaler.pkl")
    # isf = joblib.load(pwd + "hey_isloated_forest.pkl")
    # sc = joblib.load(pwd + "std_scaler.pkl")
    # y_pred = isf.predict(X)
    # word_df["y_pred"] = y_pred.tolist()
    #
    # #word_df.loc[len(word_df.index)] = ["cd",1.0396623611450195,"9:31","9","31",int(clf.predict((np.array([1.0396623611450195, '09', '31']).reshape(1, 3))))]
    # fig = px.scatter(word_df, x='time_to_write', y='time_in_day', color='y_pred',
    #                  color_continuous_scale=px.colors.diverging.RdYlGn)
    # fig.update_traces(marker=dict(size=12))
    # fig.show()
#train_ml_for_user("hey")

