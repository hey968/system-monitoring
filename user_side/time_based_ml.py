from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import plotly.express as px
import joblib
df = pd.read_csv("time_based_test.csv")
word_df = df[["command", "time_to_write", "time_in_day"]]
word_df["hour"] = word_df.time_in_day.apply(lambda x: int(x.split(":")[0]))
word_df["minute"] = word_df.time_in_day.apply(lambda x: int(x.split(":")[1]))
word_df = word_df.sort_values(by=['hour', 'minute'])
X = word_df.iloc[:,[1,3,4]].values

print(X)
sc = StandardScaler()
X = sc.fit_transform(X)
clf = IsolationForest(random_state=42,contamination=0.1)
y_pred = clf.fit_predict(X)

print(clf.predict(sc.transform(np.array([0.222, '17', '50']).reshape(1, 3))))

print(clf.predict(sc.transform(np.array([0.215, '7', '54']).reshape(1, 3))))
print(clf.predict(sc.transform(np.array([0.8, '4', '54']).reshape(1, 3))))
joblib.dump(clf,"isloated_forest.pkl")
joblib.dump(sc,"std_scaler.pkl")
word_df["y_pred"] = y_pred.tolist()


fig = px.scatter(word_df, x='time_to_write', y='time_in_day', color='y_pred',
                 color_continuous_scale=px.colors.diverging.RdYlGn)
fig.update_traces(marker=dict(size=12))
fig.show()
