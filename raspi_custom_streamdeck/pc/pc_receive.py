import socket
import keyboard
from time import *
import os
import webbrowser

key = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("add your pi's ip here", 5000))
print("connected")

while True:
    key = str(s.recv(1024).decode("utf-8"))
    
    if key == '/':
        keyboard.send("ctrl+shift+escape")
    elif key == '8':
        os.system('start chrome')
    elif key == '5':
        keyboard.send("win")
        sleep(0.05)
        keyboard.send("w+a+r")
        sleep(0.5)
        keyboard.send("enter")
    elif key == '2':
        webbrowser.get(put your chrome.exe path here).open("https://twitch.tv")
    elif key == '.':
        webbrowser.get(put your chrome.exe path here).open("https://youtube.com")
    elif key == '0':
        webbrowser.get(put your chrome.exe path here).open("https://web.whatsapp.com")
    elif key == '1':
        os.system(r'rundll32.exe powrprof.dll,SetSuspendState Hibernate')
