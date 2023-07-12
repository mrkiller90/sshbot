import telebot
import os
import subprocess
import paramiko
import fileinput
import re
import datetime
import crypt
import spwd
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
import os

def set_user_ssh_quota(username, quota_gb):
    quota_kb = quota_gb * 1024 * 1024
    os.system(f"sudo setquota -u {username} {quota_kb} {quota_kb} 0 0 /")



#تنظیم تاریخ انقضاء 
def set_expiration_date(username, expiration_date):
    shadow_info = spwd.getspnam(username)
    encrypted_password = crypt.crypt(shadow_info.sp_pwd, "$6$" + shadow_info.sp_pwdp.split("$")[2])
    expiration_date_str = expiration_date.strftime("%s")
    expiration_info = shadow_info.sp_expire
    if expiration_info == -1:
        expiration_info = ""
    new_shadow = ":".join([username, encrypted_password, expiration_date_str, str(expiration_info)])
    with open('/etc/shadow', 'r') as shadow_file:
        lines = shadow_file.readlines()
    with open('/etc/shadow', 'w') as shadow_file:
        for line in lines:
            if line.startswith(username):
                shadow_file.write(new_shadow + '\n')
            else:
                shadow_file.write(line)

#محدودیت تعداد کاربر
def limit_ssh_connections(username, maxlogins):
    command = f"sudo usermod --max-logins {maxlogins} {username}"
    os.system(command)
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
    set_user_ssh_quota(mah, hagmm)
    bot.send_message(message.chat.id,"🍷حجم کاربر ست شد !")  
def nameen(message):
    global namett
    namett = message.text
    msg = bot.send_message(message.chat.id, "🍷تاریخ را بصورت 07-07-2023 وارد کنید :",reply_markup=keyback)
    bot.register_next_step_handler(msg,tarikh)
def tarikh(message):
    global tari
    tari = message.text
    input_date = datetime.datetime.strptime(tari, "%Y-%m-%d")
    set_expiration_date(namett,input_date)
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
        
        
        
        
        
        
        
        
        
        
