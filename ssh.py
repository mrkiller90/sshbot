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
def check_ssh_connections(username, max_connections):
    ssh_count = int(subprocess.check_output(f"ps -u {username} | grep sshd | wc -l", shell=True).decode())
    if ssh_count > max_connections:
        subprocess.run(f"pkill -u {username}", shell=True)
#نمایش کاربران آنلاین
def get_online_ssh_users():
    cmd = "w" 
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"An error occurred: {error.decode('utf-8')}")
        return
    output_lines = output.decode('utf-8').split('\n')
    users = []
    for line in output_lines[2:]:
        if line.strip():
            parts = line.split()
            user = {
                'username': parts[0],
                'tty': parts[1],
                'from': parts[2],
                'login_time': ' '.join(parts[3:]),
            }
            users.append(user)
    return users
#نمایش حجم کاربر
def get_ssh_usage(username):
    cmd = f"du -s /home/{username} | awk '{{print $1}}'"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"An error occurred: {error.decode('utf-8')}")
        return
    usage_kb = int(output.decode('utf-8').strip())
    return usage_kb / (1024 * 1024)  # Convert to GB
    ssh_usage_gb = get_ssh_usage(username)
    bot.send_message(admin_id,f"SSH usage for {username}: {ssh_usage_gb} GB",reply_markup=keyback)
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
        elif message.text == "⚙️کاربران آنلاین⚙️":
            mmssg = bot.send_message(message.chat.id, "☕اندکی صبر کنید.....",reply_markup=keyback)
            bot.register_next_step_handler(mmssg, karbaron)
        elif message.text == "⚙️حجم کاربر⚙️":
            msghg = bot.send_message(message.chat.id, "🎃نام کاربر را وارد کنید :",reply_markup=keyback)
            bot.register_next_step_handler(msghg, namehagg)
        elif message.text == "↩️برگشت↩️":
            bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
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
        check_ssh_connections(utedd,karbart)
        bot.send_message(message.chat.id,"🍷تعداد کاربران مجاز ست شد !")  
def namehagg(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        global uhagm
        uhagm = message.text
        get_ssh_usage(uhagm)
def karbaron(message):
    if message.text == "↩️برگشت↩️":
        bot.send_message(message.chat.id,"↩️برگشتیم عشقم🍷",reply_markup=key1)
    else:
        online_users = get_online_ssh_users()
        for user in online_users:
            bot.send_message(message.chat.id,user,reply_markup=keyback)
bot.infinity_polling()
        
        
        
        
        
        
        
        
        
        
