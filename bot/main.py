import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
from os import environ as env
import sqlite3
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import os
import psycopg2
import os
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor
import threading

token = env["VK_TOKEN"]

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

result = urlparse(os.environ["DATABASE_URL"])
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
conn = psycopg2.connect(
    database = database,
    user = username,
    password = password,
    host = hostname,
    port = port
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

def send_message(id, message):
    print("send "+message)
    vk.method('messages.send', {'user_id': id, 'message': message, "v":'5.69'})

def reactions(event):
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me and event.from_user:
            request = event.text
            if(request == "/get"):
                dr = webdriver.Chrome()
                uid = event.user_id
                cursor.execute("SELECT * FROM auth_system_mosuser")
                all_users = cursor.fetchall()

                mosLogin = None
                mosPassword = None
                length = 0
                founded = False

                for user in all_users:
                    length += 1
                number = 0
                for user in all_users:
                    number += 1
                    try:
                        cipher = AES.new(pad(str(uid).encode(), 16), AES.MODE_EAX, user['mosPasswordNonce'])
                        mosPassword = cipher.decrypt_and_verify(user['mosPasswordCiphertext'], user['mosPasswordTag']).decode()
                        mosLogin = user['mosLogin']
                        founded = True
                    except ValueError:
                        founded = False
                        if number == length:
                            send_message(event.user_id, "blbns uf[")

                if founded:    
                    send_message(event.user_id, mosLogin+", "+mosPassword)

                #subject name mark.parent.parent.parent.parent.parent.findChild("div", {"class":"subject"})
                #date  mark.parent.parent.parent.parent.parent.parent.parent.findChildren("div")[0].findChildren("h3")[0].text
                #link ezhd https://www.mos.ru/pgu/ru/application/dogm/journal/

                    #auth
                    dr.get("https://www.mos.ru/pgu/ru/application/dogm/journal/")
                    dr.find_element_by_id('login').send_keys(mosLogin)
                    dr.find_element_by_id('password').send_keys(mosPassword)
                    dr.find_element_by_id('bind').submit()

                    sleep(15)

                    bs = BS(dr.page_source, "html.parser")

                    marks = bs.findAll("span", {"class":"mark-value"})
                    for mark in marks:
                        subject = mark.parent.parent.parent.parent.parent.findChildren("div", {"class":"subject"})[0].findChildren("div")[0].findChildren("div")[0].findChildren("span")[0]
                        date = mark.parent.parent.parent.parent.parent.parent.parent.findChildren("div")[0].findChildren("h3")[0]
                        send_message(event.user_id, date.text + " " + subject.text + " " + mark.text)

                    l = dr.find_element_by_xpath('//mat-icon[@aria-label="logout"]')
                    l.click()

                    dr.delete_all_cookies()

                    send_message(event.user_id, "done")
            else:
                send_message(event.user_id, "Ты ввёл что-то не то! Попробуй ещё раз.")

for event in longpoll.listen():
    threading.Thread(target=reactions, args=(event,)).start()