import pandas as pd

df = pd.read_csv("hey_time_based_test.csv")

new_column = []
hour = ["00", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
        "20", "21", "22", "23"]
minute = ["00"]
for j in range(1, 60):
    if j < 10:
        minute.append("0" + str(j))
    else:
        minute.append(str(j))
stop = len(df)
i = 0
ihour = 0
while i < stop:
    for iminute in minute:
        new_column.append(hour[ihour] + ":" + iminute)
        i = i + 1
        if i == stop:
            break
    ihour += 1
    if i == stop:
        break

df["time_in_day"] = new_column
df.to_csv("hey_time_based_test.csv", index=False, header=True)
