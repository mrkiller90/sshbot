import telebot
import os
import subprocess
import paramiko
import fileinput
import re
print("Wellcome To Mr-Killer Bot Script !\n id : @Mr_Killer_1\n")
portt = input("Enter Your Server Port : ")
host = input("Enter Your Domin(no http) : ")
bannert = input("Enter Banner Text : ")
token = input("Enter Bot Token : ")
adminid = input("Enter Admin ID : ")
admin_id = int(adminid)
#ساخت یوزر
def create_user(username, password):
    command = f'sudo useradd -m -p $(openssl passwd -1 {password}) -s /sbin/nologin {username}'
    os.system(command)
#دیلیت یوزر
def delete_user(username):
    os.system(f'sudo userdel {username}')
#محدودیت حجم
def set_quota(username, max_size):
    subprocess.run(['sudo', 'quotaon', '-avug'])
    subprocess.run(['sudo', 'edquota', '-u', username])
    subprocess.run(['sudo', 'quotacheck', '-m', '-avug'])
    subprocess.run(['sudo', 'quota', '-u', username, max_size])
#تنظیم تاریخ انقضاء 
def set_ssh_user_expiry(user, expiry_date):
    command = f"sudo chage -E {expiry_date} {user}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("تاریخ انقضاء کاربر SSH با موفقیت تغییر یافت.")
    else:
        print("مشکلی در تغییر تاریخ انقضاء کاربر SSH رخ داد.")

#محدودیت تعداد کاربر
def limit_ssh_connections(username, max_connections):
    command = f"sudo -u {username} sed -i 's/^MaxSessions.*/MaxSessions {max_connections}/' /etc/ssh/sshd_config"
    subprocess.run(command, shell=True)
    subprocess.run("sudo systemctl restart sshd", shell=True)
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
def info(message):
    if message.chat.id == admin_id: 
        if message.text == "✍️افزودن کاربر✍️":
            msg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msg, name)
        elif message.text == "✍️حذف کاربر✍️":
            mssg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(mssg,nameeed)
        elif message.text == "⚙️محدودیت حجم⚙️":
            msg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msg, nameha)
        elif message.text == "⚙️تاریخ انقضاء⚙️":
            msg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msg, nameen)
        elif message.text == "⚙️تعداد کاربر⚙️":
            msg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msg, nametedd)
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
    create_user(namek,ramzk)
    bot.send_message(message.chat.id,"☠️your user has been created✅"+"\n💥username :" " " + namek+"\n💥password :" " " + ramzk +"\n🔗Link :"+" "+"ssh://"+namek+":"+ramzk+"@"+host+":"+portt+"#"+namek)
def nameeed(message):
    global dellu
    dellu = message.text
    delete_user(dellu)
    bot.send_message(message.chat.id,"👹حله پدرش یام‌ یام شد!")
def nameha(message):
    global mah
    mah = message.text
    msg = bot.send_message(message.chat.id, "⚙️حجم مصرفی را وارد کنید : ",reply_markup=keyback)
    bot.register_next_step_handler(msg,hagm)
def hagm(message):
    global hagmm
    hagmm = message.text
    maxz = str(hagm) + "G"
    set_quota(mah, maxz)
    bot.send_message(message.chat.id,"🍷حجم کاربر ست شد !")  
def nameen(message):
    global namett
    namett = message.text
    msg = bot.send_message(message.chat.id, "🍷تاریخ را بصورت 07-07-2023 وارد کنید :",reply_markup=keyback)
    bot.register_next_step_handler(msg,tarikh)
def tarikh(message):
    global tari
    tari = message.text
    set_ssh_user_expiry(namett,tarikh)
    bot.send_message(message.chat.id,"🍷تاریخ کاربر ست شد !")  
def nametedd(message):
    global utedd 
    utedd = message.text
    msg = bot.send_message(message.chat.id, "🍷تعداد کاربران مجاز را وارد کنید : ",reply_markup=keyback)
    bot.register_next_step_handler(msg,tedu)
def tedu(message):
    global tedaddy 
    tedaddy = message.text
    karbart = int(tedaddy)
    limit_ssh_connections(utedd,karbart)
    bot.send_message(message.chat.id,"🍷تعداد کاربران مجاز ست شد !")  







bot.infinity_polling()
        
        
        
        
        
        
        
        
        
        
