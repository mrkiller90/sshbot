import telebot
import os
import subprocess
import paramiko
print("Wellcome To Mr-Killer Bot Script !\n id : @Mr_Killer_1\n")
portt = input("Enter Your Server Port : ")
host = input("Enter Your Domin(no http) : ")
banner = input("Enter Banner Text : ")
token = input("Enter Bot Token : ")
admin_id = input("Enter Admin ID : ")
passw = input("Enter Your Root Password : ")
#تنظیم تاریخ انقضاء 
def set_account_expiration(username, date):
    command = f"chage -E {date} {username}"
    try:
        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        error_message = e.output.decode('utf-8')
        print(f"An error occurred while setting the account expiration date: {error_message}")
#محدودیت تعداد کاربر
def limit_ssh_connections(username, max_connections):
    command = f"sudo -u {username} sed -i 's/^MaxSessions.*/MaxSessions {max_connections}/' /etc/ssh/sshd_config"
    subprocess.run(command, shell=True)
    subprocess.run("sudo systemctl restart sshd", shell=True)
#ساخت یوزر
def create_user(username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('hostname', port=portt, username='root', password=passw)
    create_user_command = f'useradd -s /usr/sbin/nologin {username}'
    stdin, stdout, stderr = client.exec_command(create_user_command)
    set_password_command = f'echo {password} | passwd {username} --stdin'
    stdin, stdout, stderr = client.exec_command(set_password_command)
    client.close()
#رمزنگاری ssh
def replace_line(filepath, pattern, replacement):
    for line in fileinput.input(filepath, inplace=True):
        updated_line = re.sub(pattern, replacement, line)
        print(updated_line, end='')
sshd_config_file = '/etc/ssh/sshd_config'
pattern = r'^# Ciphers and keying'
replacement = 'Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes256-ctr'
def check_line(filepath, pattern):
    for line in fileinput.input(filepath):
        if re.search(pattern, line):
            return True
    return False
if not check_line(sshd_config_file, replacement):
    replace_line(sshd_config_file, pattern, replacement)
#تنظیم متن بنر 
os.system("rm -r /root/banner.txt")
f = open("/root/banner.txt", "a+")
f.write(bannert)
f.close()
#شروع ربات
bot = telebot.TeleBot(token)  
key1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
key1.add("✍️افزودن کاربر✍️","✍️حذف کاربر✍️","⚙️محدودیت حجم⚙️","⚙️تاریخ انقضاء⚙️")
keyback = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
keyback.add("↩️برگشت↩️")
@bot.message_handler(commands=["start"])
def wellcome(message):
	if message.chat.id == admin_id: 
        bot.send_message(message.chat.id, "😃سلام عشقم", reply_markup=key1)
@bot.message_handler()
if message.chat.id == admin_id: 
        if message.text == "✍️افزودن کاربر✍️":
            msg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msg, name)
        elif message.text == "✍️حذف کاربر✍️":
            mssg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(mssg, namede)
        elif message.text == "⚙️محدودیت حجم⚙️":
        	msg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msg, nameha)
        elif message.text == "⚙️تاریخ انقضاء⚙️":
        	msg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msg, nameen)
def name(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global namek 
        namek = message.text
        msg = bot.send_message(message.chat.id, "🎃رمز کاربر را وارد کنید : ",reply_markup=keyback)
        bot.register_next_step_handler(msg, ramz)  
def ramz(message):
	global ramzk
    ramzk = message.text
	create_user(namek, ramzk)
    bot.send_message(message.chat.id,"☠️your user has been created✅"+"\n💥username :" " " + namek+"\n💥password :" " " + ramzk +"\n🔗Link :"+" "+"ssh://"+namek+":"+ramzk+"@"+host+":"+portt+"#"+namek)
bot.infinity_polling()
        
        
        
        
        
        
        
        
        
        