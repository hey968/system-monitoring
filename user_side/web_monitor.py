import subprocess
import pandas as pd
import vt
import os

api_key = "481dd6de4fdd15b55ac72eb034273e3cd79545e662f6d1e75743dbd2b3b3f3f8"
client = vt.Client(api_key)

if os.path.exists("web_checker.csv"):
    unsafe_web_df = pd.read_csv("web_checker.csv")
else:
    unsafe_web_df = pd.DataFrame(columns=["website name", "protocol", "reason"])


def get_http_s_connection():
    """
    check if website is unsafe in case its true its add the website to dataframe for admin check
    :return:
    """
    netstat_output = subprocess.check_output(["netstat ", "-tn"]).decode().split("\n")[5:]
    http_and_ssl_ports = [i for i in netstat_output if "443 " in i or "80 " in i]
    with open("c:\Windows\System32\Drivers\etc\hosts", "r") as fd:
        hosts_file = fd.read()
    for i in http_and_ssl_ports:
        netstat_http_ssl_line_ = i.split()
        ip = netstat_http_ssl_line_[2].split(":")[0]
        if ip in hosts_file:
            continue
        else:
            if "443 " in netstat_http_ssl_line_[2]:
                dns = subprocess.check_output(["nslookup", "ip"]).decode().split("\n")[3].split(" ")[-1][:-1]
                vt_result_id = vt.url_id("https://" + dns)
                vt_result = client.get_object("/urls/{}", vt_result_id)
                if vt_result.last_analysis_stats["malicious"] != 0 or vt_result.last_analysis_stats["suspicious"] != 0:
                    unsafe_web_df.loc[len(unsafe_web_df.index)] = [vt_result.last_final_url[vt_result.last_final_url.find("/")+2:vt_result.last_final_url.rfind("/")],
                                             "https",
                                             "virus total scan the following website and found out this website isn't safe"]
                    unsafe_web_df.to_csv("web_checker.csv", index=False, header=True)
            elif "80 " in netstat_http_ssl_line_[2]:
                unsafe_web_df.loc[len(unsafe_web_df.index)] = [dns, "http","this website use http which isn't secure protocol"]
                unsafe_web_df.to_csv("web_checker.csv", index=False, header=True)



def main():
    """
    call the function get_http_s_connection
    :return:
    """
    while True:
        pass
        #for demonstrate uncomment the line below
        #get_http_s_connection()
if __name__ == "__main__":
    main()
