import subprocess
import time
subprocess.call(["clear"])
print("Wellcome To X-Killer Bot Script !\n id : @Mr_Killer_1 And @Amirwopi_Fox\n")
time.sleep(5)
subprocess.run(["sudo", "apt-get", "remove", "python3.8" , "-y"])
subprocess.run(["sudo", "apt-get", "remove", "python3-pip", "-y"])
subprocess.run(["sudo", "apt-get", "update"])
subprocess.run(["sudo", "apt", "install", "python3", "-y"])
subprocess.run(["sudo", "apt", "install", "python3-pip", "-y"])
subprocess.run(["pip", "install", "telebot"])
subprocess.run(["pip", "install", "paramiko"])
subprocess.run(["sudo", "apt", "install", "screen", "-y"])
subprocess.call(["clear"])
subprocess.run(["cp", "ssh.py", "/root"])

bash_script = """
#!/bin/bash

clear
udpport=7300
read -p "Port UDPGW Vared konid (besorat pishfarz in port mibashad ${udpport}): " udpport

apt update -y
apt install git cmake -y

git clone https://github.com/ambrop72/badvpn.git /root/badvpn

mkdir /root/badvpn/badvpn-build
cd /root/badvpn/badvpn-build

cmake .. -DBUILD_NOTHING_BY_DEFAULT=1 -DBUILD_UDPGW=1 > cmake_output.txt 2>&1 &&
make > make_output.txt 2>&1 &&

cp udpgw/badvpn-udpgw /usr/local/bin

cat > /etc/systemd/system/videocall.service << ENDOFFILE
[Unit]
Description=UDP forwarding for badvpn-tun2socks
After=nss-lookup.target

[Service]
ExecStart=/usr/local/bin/badvpn-udpgw --loglevel none --listen-addr 127.0.0.1:${udpport} --max-clients 999
User=videocall

[Install]
WantedBy=multi-user.target
ENDOFFILE

useradd -m videocall
systemctl enable videocall
systemctl start videocall
"""

subprocess.run(["bash", "-c", bash_script])
subprocess.run(["screen", "sudo", "python3", "/root/ssh.py"], capture_output=True)
