import os
import sys
import subprocess
import shutil
from datetime import datetime

rootLogDir = "/var/log/SysAdmin-Logs"
installationLogDir = "/var/log/SysAdmin-Logs/Installations"
updateLogDir = "/var/log/SysAdmin-Logs/Updates"
subLogDirPath = [installationLogDir, updateLogDir]

installation_log_file = "install.log"
update_log_file = "update.log"
installation_path = os.path.join(installationLogDir,installation_log_file)
update_path = os.path.join(updateLogDir,update_log_file)
file_paths = [installation_path, update_path]

updates = ["apt-get update -y", "apt-get upgrade -y", "apt-get dist-upgrade -y", "apt-get clean", "apt-get autoremove -y"]

def check_root():
    if os.getuid() != 0:
        print("This script must be run as root", file=sys.stderr)
        sys.exit(1)

                
def rootLogDirValidation(path):   
    if not os.path.exists(path):
        print("Log path does not exist")
        print("Creating path")
        try:
           os.makedirs(path)
           print(f"{path} has been created")
        except Exception as e:
           print(f"An error has occured: {e}")

def subLogDirValidation(path_lst):
    for i in path_lst:
        if not os.path.exists(i):
            print("Log path does not exist")
            print(f"Creating path: {i}")
            try:
                os.makedirs(i)
                print(f"{i} has been created")
            except Exception as e:
                print(f"An error has occured: {e}")

def validateLogFile(path_lst):
    for i in path_lst:
        if not os.path.isfile(i):
            try:
                with open(i, "w") as f:
                    pass
            except Exception as e:
                print(f"An error has occurred in creating log file: {e}")

def runUpdates(lst):
    for i in lst:
        command = ["bash", "-c", i]
        try:
            subprocess.run(command, check=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(update_path, "a") as f:
                f.write(f"{timestamp} - Success: {i}\n")
            print(f"Success: {i}")
        except subprocess.CalledProcessError:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(update_path, "a") as f:
                f.write(f"{timestamp} - Failed: {i}\n")
            print(f"Failed: {i}")

def installNmap():
    install_nmap = ["apt", "install", "-y", "nmap"]
    if shutil.which("nmap") is not None:
            print("Nmap is already installed.")
    try:
        subprocess.run(install_nmap, check=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(installation_path, "a") as f:
            f.write(f"{timestamp} - Success: apt install -y nmap\n")
        print(f"Success: Nmap installed")
    except subprocess.CalledProcessError:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(installation_path, "a") as f:
            f.write(f"{timestamp} - Failed: apt install -y nmap\n")
        print(f"Failed: Nmap installation")


check_root()
rootLogDirValidation(rootLogDir)
subLogDirValidation(subLogDirPath)
validateLogFile(file_paths)
runUpdates(updates)
installNmap()