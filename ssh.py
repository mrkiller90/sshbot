import telebot
import os
import subprocess
import paramiko
import fileinput
import re
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
def set_user_ssh_quota(username, quota_gb):
    quota_kb = quota_gb * 1024 * 1024
    os.system(f"sudo setquota -u {username} {quota_kb} {quota_kb} 0 0 /")
#تنظیم تاریخ انقضاء 
def change_expiration(username, expiration_date):
    command = f"sudo chage -E {expiration_date} {username}"
    subprocess.call(command, shell=True)
#محدودیت تعداد کاربر
def limit_ssh_connections(username, max_sessions):
    command = f"sed -i 's/^#MaxSessions.*$/MaxSessions {max_sessions}/' /etc/ssh/sshd_config"
    subprocess.run(['bash', '-c', command])
    restart_command = "service ssh restart"
    subprocess.run(['bash', '-c', restart_command])
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
f = open("banner.txt", "a+")
f.close()
def replace_line(filepathh, patternn, replacementt):
    for line in fileinput.input(filepathh, inplace=True):
        updated_line = re.sub(patternn, replacementt, line)
        print(updated_line, end='')
sshd_config_file = '/etc/ssh/sshd_config'
patternn = r'^#Banner none'
replacement = 'Banner /root/banner.txt'
def check_line(filepathh, patternn):
    for line in fileinput.input(filepathh):
        if re.search(patternn, line):
            return True
    return False
if not check_line(sshd_config_file, replacementt):
    replace_line(sshd_config_file, patternn, replacementt)
#شروع ربات
bot = telebot.TeleBot(token)  
key1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
key1.add("✍️افزودن کاربر✍️","✍️حذف کاربر✍️","⚙️محدودیت حجم⚙️","⚙️تاریخ انقضاء⚙️","⚙️تعداد کاربر⚙️")
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
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global ramzk
        ramzk = message.text
        create_user(namek,ramzk)
        bot.send_message(message.chat.id,"☠️your user has been created✅"+"\n💥username :" " " + namek+"\n💥password :" " " + ramzk +"\n🔗Link :"+" "+"ssh://"+namek+":"+ramzk+"@"+host+":"+portt+"#"+namek)
def nameeed(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global dellu
        dellu = message.text
        delete_user(dellu)
        bot.send_message(message.chat.id,"👹حله پدرش یام‌ یام شد!")
def nameha(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global mah
        mah = message.text
        msg = bot.send_message(message.chat.id, "⚙️حجم مصرفی را وارد کنید : ",reply_markup=keyback)
        bot.register_next_step_handler(msg,hagm)
def hagm(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global hagmm
        hagmm = message.text
        set_user_ssh_quota(mah, hagmm)
        bot.send_message(message.chat.id,"🍷حجم کاربر ست شد !")  
def nameen(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global namett
        namett = message.text
        msg = bot.send_message(message.chat.id, "🍷تاریخ را بصورت 07-07-2023 وارد کنید :",reply_markup=keyback)
        bot.register_next_step_handler(msg,tarikh)
def tarikh(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global tari
        tari = message.text
        change_expiration(namett,tari)
        bot.send_message(message.chat.id,"🍷تاریخ کاربر ست شد !")  
def nametedd(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global utedd 
        utedd = message.text
        msg = bot.send_message(message.chat.id, "🍷تعداد کاربران مجاز را وارد کنید : ",reply_markup=keyback)
        bot.register_next_step_handler(msg,tedu)
def tedu(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global tedaddy 
        tedaddy = message.text
        karbart = int(tedaddy)
        limit_ssh_connections(utedd,karbart)
        bot.send_message(message.chat.id,"🍷تعداد کاربران مجاز ست شد !")  
bot.infinity_polling()
        
        
        
        
        
        
        
        
        
        
