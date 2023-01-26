from admin_side.app import run_app
from user_side.cmd_shell import build
from user_side.rdp_file_system_monitoring import main as rdp_file_system
from user_side.web_monitor import main as web_monitor
from threading import Thread


def main():
    theards = []
    theard1=Thread(target=web_monitor)
    theard3 = Thread(target=build)
    theard4=Thread(target=run_app)
    theard2=Thread(target=rdp_file_system,args=("",))
    theards.append(theard1)
    theards.append(theard2)
    theards.append(theard3)
    theards.append(theard4)
    for t in theards:
        t.start()




if __name__ == "__main__":
    main()