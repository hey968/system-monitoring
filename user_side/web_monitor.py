import subprocess
import pandas as pd
import vt
import os

api_key = "481dd6de4fdd15b55ac72eb034273e3cd79545e662f6d1e75743dbd2b3b3f3f8"
client = vt.Client(api_key)

if os.path.exists("web_checker.csv"):
    df = pd.read_csv("web_checker.csv")
else:
    df = pd.DataFrame(columns=["website name", "protocol", "reason"])


def get_https_s_connection():
    proc = subprocess.check_output(["netstat ", "-tn"]).decode().split("\n")[5:]
    http_s_list = [i for i in proc if "443 " in i or "80 " in i]
    for i in http_s_list:
        line_list = i.split()
        ip = line_list[2].split(":")[0]
        with open("c:\Windows\System32\Drivers\etc\hosts", "r") as fd:
            file_read = fd.read()
            if ip in file_read:
                continue
            else:
                if "443 " in line_list[2]:
                    dns = subprocess.check_output(["nslookup", "ip"]).decode().split("\n")[3].split(" ")[-1][:-1]
                    result_code = vt.url_id("https://" + dns)
                    result = client.get_object("/urls/{}", result_code)
                    if result.last_analysis_stats["malicious"] != 0 or result.last_analysis_stats["suspicious"] != 0:
                        df.loc[len(df.index)] = [result.last_final_url[result.last_final_url.find("/")+2:result.last_final_url.rfind("/")], "https",
                                                 "virus total scan the following website and found out this website isn't safe"]
                        df.to_csv("web_checker.csv", index=False, header=True)
#todo send to admin panel for check
                elif "80 " in line_list[2]:
                    df.loc[len(df.index)] = [dns, "http",
                                             "this website use http which isn't secure protocol"]
                    df.to_csv("web_checker.csv", index=False, header=True)
# todo send it to admin panel for check


def main():
    while True:
        pass
if __name__ == "__main__":
    main()
