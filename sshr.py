import os
import time
os.system("clear")
print("Wellcome To Mr-Killer Bot Script !\n id : @Mr_Killer_1\n")
time.sleep(5)
os.system("sudo apt-get update")
os.system("sudo apt install python3-pip -y")
os.system("pip install telebot")
os.system("pip install paramiko")
os.system("sudo apt install screen -y")
os.system("bash <(curl -Ls https://raw.githubusercontent.com/Alirezad07/X-Panel-SSH-User-Management/master/fix-call.sh --ipv4)")
os.system("clear")
os.system("cp ssh.py /root")
os.system("cd /root && screen sudo python3 ssh.py ")