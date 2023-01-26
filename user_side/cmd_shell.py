import os
from tkinter import Tk, Text, END, BOTH, messagebox
import time
import pandas as pd
import datetime
import json
import joblib
import numpy as np
from user_side.time_based_ml import train_ml_for_user

pressed_once = True
start_time = 0
command_recorded = False

# configure
def get_conf():
    cwd = os.getcwd()
    return cwd[:cwd.rfind("project")+len("project")] + "\\user_side\\configure.json"
with open(get_conf(), "r") as fd:
    json_data = json.load(fd)
username = os.getlogin()
pwd = json_data["user_side_loc"]
ml_phase = json_data[username][0]["learning_phase"]
isf = joblib.load(pwd + username + "_isloated_forest.pkl")


# wait for confirmation from admin to let the user use the cmd
def wait_for_confirmation():
    df2 = pd.read_csv(pwd + "user_anomaly_detection.csv")
    if df2['accept'][0] == 1:
        df2 = df2.drop(0)
        df2.to_csv(pwd + "user_anomaly_detection.csv", index=False, header=True)
        cmd.deiconify()
        return
    cmd.after(5, wait_for_confirmation)


# check for anomaly in the user time writing
def user_anomaly(command):
    hour_and_minute = datetime.datetime.now().strftime("%H:%M").split(":")
    data = [time.time() - start_time, hour_and_minute[0],
            hour_and_minute[1]]
    result = isf.predict(np.array(data).reshape(1, 3))
    print(data, result)
    if result == -1:
        df2 = pd.read_csv(pwd + "user_anomaly_detection.csv")
        df2.loc[len(df2.index)] = [username, command, os.getcwd()] + data + [0]
        df2.to_csv(pwd + "user_anomaly_detection.csv", index=False, header=True)
        df2 = pd.read_csv(pwd + "user_anomaly_detection.csv")
        cmd.withdraw()
        wait_for_confirmation()


# when the command is one word like cd
def one_word_command(e):
    global start_time
    global command_recorded
    global ml_phase
    global isf
    user_command = cmd_text.get('end -1 lines', END)
    user_command = user_command[user_command.find("> ") + 2:]
    if ml_phase:
        if os.path.exists(pwd + username + "_time_based_test.csv"):
            df = pd.read_csv(pwd + username + "_time_based_test.csv")
        else:
            df = pd.DataFrame(columns=["user_name", "command", "time_to_write", "time_in_day"])
        if not command_recorded:
            df.loc[len(df.index)] = [username, user_command[:user_command.find(" ")], time.time() - start_time,
                                     datetime.datetime.now().strftime("%H:%M")]
            df.to_csv(pwd + username + "_time_based_test.csv", index=False, header=True)
            if len(df.index) == 1440:
                train_ml_for_user(username)
                isf = joblib.load(pwd + username + "_isloated_forest.pkl")
                json_data[username]["learning_phase"] = False
                ml_phase = False
    else:
        if not command_recorded:
            user_anomaly(user_command)

    command_recorded = False

    if "cd " in user_command:
        try:
            os.chdir(user_command[3:-1])
            return_command = ""
        except:
            return_command = ""
    else:
        try:
            return_command = str(os.popen(user_command).read())
        except:
            return_command = "error\n"
    cmd_text.insert(END, "\n" + return_command)
    cmd_text.insert(END, str(os.getcwd()) + " > ")
    cmd_text.mark_set('insert', 'end')
    cmd_text.yview_pickplace("end")
    return 'break'


# when the command is continue for options like arp -a
def command_with_options(e):
    global start_time
    global command_recorded
    global ml_phase
    global isf
    if not command_recorded:
        user_command = cmd_text.get('end -1 lines', END)
        user_command = user_command[user_command.find("> ") + 2:]
        if ml_phase:
            if os.path.exists(pwd + username + "_time_based_test.csv"):
                df = pd.read_csv(pwd + username + "_time_based_test.csv")
            else:
                df = pd.DataFrame(columns=["user_name", "command", "time_to_write", "time_in_day"])
            df.loc[len(df.index)] = [username, user_command[:user_command.find(" ")], time.time() - start_time,
                                     datetime.datetime.now().strftime("%H:%M")]
            df.to_csv(pwd + +username + "_time_based_test.csv", index=False, header=True)
            if len(df.index) == 1440:
                train_ml_for_user(username)
                isf = joblib.load(pwd + username + "_isloated_forest.pkl")
                json_data[username]["learning_phase"] = False
                ml_phase = False
        else:
            user_anomaly(user_command)

        command_recorded = True


# prevent from deleting the current working folder
def prevent_deleting(e):
    if cmd_text.get('end -1 lines', END)[:-1] in str(os.getcwd()) + " > ":
        return 'break'


# start the timer and prevent editing of older output
def prevent_editing(e):
    global pressed_once
    global start_time
    if pressed_once:
        start_time = time.time()
    cmd_text.mark_set('insert', 'end')

def build():
    global cmd
    global cmd_text
    cmd = Tk()
    cmd.withdraw()

    df2 = pd.read_csv(pwd + "user_anomaly_detection.csv").to_dict()
    if df2['accept'] and df2["accept"][0] == 0:
        messagebox.showwarning("wait for Confirmation",
                               "The system detected an exception,please wait for Confirmation from admin")
        raise SystemExit

    cmd.deiconify()
    cmd.geometry('1000x600')
    cmd.configure(bg="black")
    cmd_text = Text(cmd, bg="black", fg="white", insertbackground="white", font=("Consolas", 16))
    cmd_text.bind("<Return>", one_word_command)
    cmd_text.bind('<BackSpace>', prevent_deleting)
    cmd_text.bind('<Key>', prevent_editing)
    cmd_text.bind("<space>", command_with_options)
    cmd_text.pack(expand=True, fill=BOTH)
    cmd_text.insert(END, str(os.getcwd()) + " > ")
    cmd.mainloop()

if __name__ == '__main__':
    build()