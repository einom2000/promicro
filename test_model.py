import win32gui
import time
import win32api
import random
import pyautogui
import psutil
import sys
import pyttsx3
import winshell
import os
import keyboard
from bt_log_in import *


acc_f = open("account.txt", "r")
acc_lines = acc_f.readlines()
account_id = acc_lines[0][:-1]
account_psd = acc_lines[1][:-1]
account_data = [account_id, account_psd]
bn_target = winshell.shortcut(os.path.join(winshell.desktop(), "暴雪战网.lnk")).path
CONFI = 0.9

# log_in(account_data, bn_target, '魔兽世界')
# print(random.uniform(2000, 4000) / 1000)
import keyboard  # using module keyboard
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('You Pressed A Key!')
            break  # finishing the loop
        else:
            pass
    except:
        break  # if us