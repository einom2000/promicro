import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import winshell, psutil
import logging, json
import cv2
from datetime import datetime
# P is for pet setting window
# F1 search the pet boss
# F2 search the the mob
# level of the first baby (329,328)(340,340)
# vs image (627, 44)(668, 69)
# roundend image (544, 695) (582, 736)p
# deadchoose image (399, 697)(558, 733)
# revival button image (642, 71)(677, 109))
#  1,4,2,2,1,2,4,3,1,3,4,2,...

logging.basicConfig(filename='leveling.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )
logging.info('Program starts!')

def find_wow_window():
    while True:
        hwndwow = win32gui.FindWindow(None, '魔兽世界')
        if hwndwow != 0:
            hwndwowrec = win32gui.GetWindowRect(hwndwow)
            print(hwndwow, hwndwowrec)
            if hwndwowrec[:2] != (0, 0):
                win32gui.MoveWindow(hwndwow, 0, 0, 1296, 759, 0)
            logging.info('wow window was set to the up left corner')
            break
    return


def found_level(level_img, position):
    found_level = pyautogui.locateCenterOnScreen(level_img,
                                                 region=position)
    return found_level


def key_2_sent(key):
    key_2_sent = str(key)
    ard.flush()
    print ("Python value sent: " + key_2_sent)
    ard.write(str.encode(key_2_sent))
    time.sleep(0.5) # I shortened this to match the new value in your Arduino code
    # waiting for pro micro to send 'Done'
    done_received = False
    while not done_received:
        original_msg = str(ard.read(ard.inWaiting())) # read all characters in buffer
        # to git rid of the serial print additional letters.
        msg = original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
        if msg[0:4] == 'Done':
            print("Message from arduino: ")
            print(msg)
            done_received = True
        else:
            ard.flush()
            time.sleep(0.3)
    return

# game parameters setup
port = 'COM10' # note I'm using Mac OS-X
ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2) # wait for Arduino
check_image = {}

find_wow_window()
print('press ctrl to start')
while not keyboard.is_pressed('ctrl'):
    pass
# checking the baby level
# key_2_sent('p')
# baby_level = 0
# for i in range(23, 26):
#     if found_level('level%s.png' % str(i), (320, 320, 350, 350)) is not None:
#         baby_level = i
#         break
# print("baby level is " + str(baby_level))




# main loop
# script_running = True
# while script_running:
#     last_revival_time = time.time()
#     # check if all the team members are alive, if not, wait for a revival
#     # check if the baby's level is less than 24, if not, change to a next baby
#     # cast macro to get the target
#     # react with the target
#     # wait and check the pbattle feature shown
#     # battle loop start
#     # loop unless the win feature shown