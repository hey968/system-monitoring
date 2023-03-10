from admin_side.app import run_app
from user_side.cmd_shell import build
from user_side.rdp_file_system_monitoring import main as rdp_file_system
from user_side.web_monitor import main as web_monitor
from multiprocessing import Process

def main():
    processes = []
    process1=Process(target=web_monitor)
    process2 = Process(target=build)
    process3=Process(target=run_app)
    process4=Process(target=rdp_file_system,args=("",))
    processes.append(process3)
    processes.append(process1)
    processes.append(process2)
    processes.append(process4)

    for p in processes:
        p.start()





if __name__ == "__main__":
    main()