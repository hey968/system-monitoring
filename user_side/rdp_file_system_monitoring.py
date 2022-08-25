from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
import datetime
import pandas as pd


# rdp monitoring

#check_port_open = ['TCP', '10.100.102.24:3389', '10.100.102.25:61519', 'ESTABLISHED']
def rdp_monitoring(current_connected_ip):
    if os.path.exists("rdp_connections.csv"):
        df = pd.read_csv("rdp_connections.csv")
    else:
        df = pd.DataFrame(columns=["ip", "date_and_time"])

    netstat_output = os.popen("netstat -an -p tcp").readlines()
    check_port_open = []
    for i in range(len(netstat_output)):
        if ":3389 " in netstat_output[i]:
            check_port_open = netstat_output[i].split()
    if len(check_port_open) == 4:
        if "3389" in check_port_open[1] and "ESTABLISHED" in check_port_open[3]:
            print(check_port_open)
            if current_connected_ip != check_port_open[2][:check_port_open[2].find(":")]:
                current_connected_ip = check_port_open[2][:check_port_open[2].find(":")]
                df.loc[len(df.index)] = [current_connected_ip, datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S')]
                df.to_csv("rdp_connections.csv", index=False, header=True)
    return current_connected_ip


# file system monitoring
def on_deleted(e):
    if os.path.exists("file_system.csv"):
        df = pd.read_csv("file_system.csv")
    else:
        df = pd.DataFrame(columns=["date_and_time", "event", "file"])
    if "file_system.csv" not in e.src_path and "rdp_connections.csv" not in e.src_path:
        df.loc[len(df.index)] = [datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S'), "deleted", str(e.src_path)]
        df.to_csv("file_system.csv", index=False, header=True)


def on_created(e):
    if os.path.exists("file_system.csv"):
        df = pd.read_csv("file_system.csv")
    else:
        df = pd.DataFrame(columns=["date_and_time", "event", "file"])
    if "file_system.csv" not in e.src_path and "rdp_connections.csv" not in e.src_path:
        df.loc[len(df.index)] = [datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S'), "created", str(e.src_path)]
        df.to_csv("file_system.csv", index=False, header=True)


def on_modified(e):
    if os.path.exists("file_system.csv"):
        df = pd.read_csv("file_system.csv")
    else:
        df = pd.DataFrame(columns=["date_and_time", "event", "file"])
    if "file_system.csv" not in e.src_path and "rdp_connections.csv" not in e.src_path:
        df.loc[len(df.index)] = [datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S'), "modified", str(e.src_path)]
        df.to_csv("file_system.csv", index=False, header=True)


def on_moved(e):
    if os.path.exists("file_system.csv"):
        df = pd.read_csv("file_system.csv")
    else:
        df = pd.DataFrame(columns=["date_and_time", "event", "file"])
    if "file_system.csv" not in e.src_path and "rdp_connections.csv" not in e.src_path:
        df.loc[len(df.index)] = [datetime.datetime.today().strftime('%d-%m-%Y, %H:%M:%S'), "moved", str(e.src_path)]
        df.to_csv("file_system.csv", index=False, header=True)


def main(current_connected_ip):
    event_handler = PatternMatchingEventHandler(patterns="*", ignore_patterns=" ", ignore_directories=False,
                                                case_sensitive=True)
    event_handler.on_deleted = on_deleted
    event_handler.on_created = on_created
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved
    path = "F:\\"
    obs = Observer()
    obs.schedule(event_handler, path, recursive=True)
    obs.start()
    while True:
        current_connected_ip = rdp_monitoring(current_connected_ip)


main("")
