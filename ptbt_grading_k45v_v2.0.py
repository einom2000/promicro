import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
import cv2, os
from datetime import datetime
import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
import cv2, os
from datetime import datetime
from tkinter import *
from PIL import Image, ImageFilter, ImageChops
import pytesseract
import numpy as np
import PIL.ImageOps
import pyperclip
import json
import pyttsx3
from win32api import GetKeyState
from win32con import VK_CAPITAL
import winshell, psutil
engine = pyttsx3.init()

# P is for pet setting window
# z search the pet boss
# x search the the mob
# c revival key
# v for confirmation button
# level of the first baby (329,328)(340,340)
# vs image (627, 44)(668, 69)
# round_end image (602, 646) (698, 677)
# dead_choose image (399, 697)(558, 733)
# revival button image (642, 71)(677, 109))
# revival c key button image (274, 657) (299, 687)
# black_teeth_2.png (432, 685)(481, 737)
# black_teeth_3.png (490, 687) (535, 734)
# rush_3.png (373, 687) (419, 735)
# add keyboard.release(all) in arduino
# rematch upleveling team auto

logging.basicConfig(filename='leveling.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )
logging.info('Program starts!')




def enumhandler(hwnd, lParam):
    # enumwindows' callback function
    # if found move to up_left corner
    if win32gui.IsWindowVisible(hwnd):
        if '魔兽世界' in win32gui.GetWindowText(hwnd):
            # rect = win32gui.GetWindowRect(hwnd)
            # print(rect[2] - rect[0], rect[3] - rect[1])
            win32gui.MoveWindow(hwnd, 0, 0, 1296, 759, True)
            # rect = win32gui.GetWindowRect(hwnd)
            # print(rect[2] - rect[0], rect[3] - rect[1])
            # print(rect)


def is_off_line():
    start_t = time.time()
    found = None
    while time.time() - start_t <= 60:
        found = pyautogui.locateCenterOnScreen('off_line_logo.png', region=OFF_LINE_LOGO_REGION,
                                               grayscale=False, confidence=0.9)
        if found is not None:
            break
    return found



def kill_process(process_name, wd_name):
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == process_name:
            proc.kill()
            break
    while win32gui.FindWindow(None, wd_name):
        pass
    return


def log_in(account):
    # open in battle net login window
    loginbt = LoginWindow(bn_target, '暴雪战网登录', account[0], account[1])
    logged_in = False
    logging_time = time.time()
    bt_window = 0
    while not logged_in:
        loginbt.runbnet()
        bn_hwnd = loginbt.findWindow()
        loginbt.login()
        # wait for the battle net window shows up
        time_login = time.time()
        while time.time() - time_login <= 50:
            bt_window = win32gui.FindWindow(None, '暴雪战网')
            if bt_window > 0:
                logged_in = True
                break
        if not logged_in:
            kill_process('Battle.net.exe', '暴雪战网登录')
        if time.time() - logging_time >= 600:
            # after 10 minutes failure, terminate program
            sys.exit()
    win32gui.SetForegroundWindow(bt_window)
    win32gui.MoveWindow(bt_window, 0, 0, 1280, 820, 1)
    bt_rec = win32gui.GetWindowRect(bt_window)

    time.sleep(1)

    while True:
        found = pyautogui.locateCenterOnScreen('bt_logged_in.png', region=BT_LOGGED_IN_REGION,
                                               grayscale=False, confidence=0.9)
        if found is not None:
            x = found[0]
            y = found[1]
            break
    pyautogui.moveTo(x, y, 1,  pyautogui.easeInQuad)
    pyautogui.click(x, y)

    # waiting for wow running
    wow_is_running = False
    wow_window = 0
    while not wow_is_running:
        wow_window = win32gui.FindWindow(None, '魔兽世界')
        if wow_window > 0:
            wow_is_running = True

    time.sleep(20)
    win32gui.EnumWindows(enumhandler, None)


class LoginWindow:

    windowHwnd = 0

    def __init__(self, programdir, windowname, username, userpwd):
        self.programDir = programdir
        self.windowName = windowname
        self.userName = username
        self.userPwd = userpwd

    def runbnet(self):
        exist = win32gui.FindWindow(None, self.windowName)
        if exist == 0:
            win32api.WinExec(self.programDir)
        return

    def findWindow(self):
        while True:
            hwndbnt = win32gui.FindWindow(None, self.windowName)
            if hwndbnt == 0:
                continue
            else:
                win32gui.MoveWindow(hwndbnt, 100, 100, 365, 541, True)
            break
        win32gui.SetForegroundWindow(hwndbnt)
        time.sleep(0.5)
        return hwndbnt

    def login(self):
        # to log in id
        for i in range(4):  # orginal 4
            pyautogui.press('tab')
            time.sleep(random.randint(3, 5) / 10)
        # clear box
        pyautogui.press('backspace')
        time.sleep(random.randint(3, 5) / 10)
        # change to english
        pyautogui.press('shift')
        time.sleep(random.randint(3, 5) / 10)
        win32api.LoadKeyboardLayout('00000409', 1)
        time.sleep(random.randint(3, 5) / 10)
        # typein
        pyautogui.typewrite(self.userName, interval=(random.randint(15, 30) / 100))
        time.sleep((random.randint(15, 30) / 100))
        pyautogui.press('tab')
        pyautogui.typewrite(self.userPwd, interval=(random.randint(15, 30) / 100))
        time.sleep(5)
        for i in range(3):
            pyautogui.press('tab')
            time.sleep(random.randint(3, 5) / 10)
        # log in
        pyautogui.press('enter')
        return


def pet_check():
    if is_it_found('2nd_pet_feature'):
        return 2
    elif is_it_found('3rd_pet_feature'):
        return 3
    elif is_it_found('1st_pet_feature'):
        return 1
    else:
        return 0


def check_level():
    bb_level = 0
    key_2_sent('p')  # p is the pet info short_key
    for i in range(23, 26):
        if found_level(check_image.get('level' + str(i)),
                       check_cord.get('level_check_box')) is not None:
            bb_level = i
            break
    logging.info("checking: baby level is " + str(bb_level))
    sleep(1200, 1400)
    key_2_sent('p')  # to close pet info window
    sleep(1200, 1400)
    return bb_level


def check_pet_alive():
    time.sleep(random.randint(2000, 3000) / 1000)
    key_2_sent('p')
    if pyautogui.locateOnScreen(check_image.get('dead_icon_on_pet_menu1'),
                                region=check_cord.get('dead_icon_on_pet_menu1'),
                                grayscale=False,
                                confidence=0.8) is not None:
        is_pets_alive[1] = False
    else:
        is_pets_alive[1] = True
    if pyautogui.locateOnScreen(check_image.get('dead_icon_on_pet_menu2'),
                                region=check_cord.get('dead_icon_on_pet_menu2'),
                                grayscale=False,
                                confidence=0.8) is not None:
        is_pets_alive[2] = False
    else:
        is_pets_alive[2] = True
    if pyautogui.locateOnScreen(check_image.get('dead_icon_on_pet_menu3'),
                                region=check_cord.get('dead_icon_on_pet_menu3'),
                                grayscale=False,
                                confidence=0.8) is not None:
        is_pets_alive[3] = False
    else:
        is_pets_alive[3] = True
    time.sleep(random.randint(1000, 2000) / 1000)
    key_2_sent('p')
    print('pet check: = ', end='')
    print(is_pets_alive)
    sleep(1200, 1400)


def check_for_attack_result():
    tm = time.time()
    while True:
        if left_pets == 3:
            if is_it_found('round_end'):
                return 1
            elif is_it_found('dead_choose'):
                return 0
            elif not is_it_found('vs_image'):
                return -1
        elif left_pets == 2:
            if is_it_found('up_dead_icon1'):
                return 99  # dead don't have to choose
            elif is_it_found('round_end'):
                return 1
            elif not is_it_found('vs_image'):
                return -1
        elif left_pets == 1:
            if is_it_found('round_end'):
                return 1
            elif not is_it_found('vs_image'):
                return -1
            elif time.time() - tm >= 7:
                return 1
        if time.time() - tm >= 15:  # in case some trick to prevent from swift team member
            return 1


def is_it_found(key):
    fd = pyautogui.locateOnScreen(check_image.get(key),
                                  region=check_cord.get(key),
                                  grayscale=False,
                                  confidence=0.8)
    print(key, fd)
    return fd


def is_debuffed():
    if is_it_found('black_teeth_buff') is not None:
        print('target is debuffed')
        return True
    else:
        print('target is not debuffed')
        return False


def sleep(millisecond1, millisecond2):
    tm = (random.randint(millisecond1 // 10, millisecond2 // 10) / 100) * 1.1
    print('wait for ' + str(tm) + ' seconds....')
    time.sleep(tm)
    return


def load_battle(enemy):
    key_2_sent(enemy)
    sleep(1200, 1500)
    key_2_sent('y')  # y is the start battle key
    sleep(1500, 2000)
    end = time.time() + 6 * 1
    fd = None
    while time.time() < end:
        fd = is_it_found('vs_image')
        if fd is not None:
            break
    return fd


def find_wow_window():
    while True:
        hwndwow = win32gui.FindWindow(None, '魔兽世界')
        if hwndwow != 0:
            hwndwowrec = win32gui.GetWindowRect(hwndwow)
            print(hwndwow, hwndwowrec)
            if os.path.basename(__file__) == 'ptbt.py':
                win32gui.MoveWindow(hwndwow, 0, 0, 1296, 759, 0)
            elif os.path.basename(__file__) == 'ptbt_sur.py':
                win32gui.MoveWindow(hwndwow, 0, 0, 988, 768, 0)
            else:
                win32gui.MoveWindow(hwndwow, 0, 0, 1296, 759, 0)
            logging.info('wow window was set to the up left corner')
            break
    return


def found_level(level_img, position):
    fd = pyautogui.locateCenterOnScreen(level_img,
                                        region=position)
    return fd


def set_all_dead():
    global is_pets_alive, left_pets, current_pet
    is_pets_alive = {1: False,
                     2: False,
                     3: False}
    left_pets = 0
    current_pet = -1


def revival():
    global is_pets_alive, last_revival_time, current_pet
    k = 1
    check_pet_alive()

    left_pets = 0
    for i in range(3):
        if is_pets_alive.get(i + 1):
            left_pets += 1
    if left_pets >= 2:
        return

    while not is_it_found('revival_c_key'):
        key_2_sent(str(k % 2 + 2))
        k += 1
        sleep(500, 800)
        check()
        pass
    key_2_sent('c')
    key_2_sent(' ')
    is_pets_alive = {1: True,
                     2: True,
                     3: True}
    logging.info('revivaled all.')

    sleep(2000, 3000)
    last_revival_time = time.time()
    current_pet = 1


def key_2_sent(key):
    key_sent = str(key)
    ard.flush()
    print ("Python value sent: " + key_sent)
    ard.write(str.encode(key_sent))
    time.sleep(0.5) # I shortened this to match the new value in your arduino code
    # waiting for pro micro to send 'Done'
    done_received = False
    while not done_received:
        original_msg = str(ard.read(ard.inWaiting())) # read all characters in buffer
        # to git rid of the serial print additional letters.
        msg = original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
        if msg[0:4] == 'Done':
            # print("Message from arduino: ")
            # print(msg)
            done_received = True
        else:
            ard.flush()
            time.sleep(0.3)
    return

def check():

    if is_off_line() is not None:
        kill_process('Wow.exe', '魔兽世界')
        time.sleep(10)
        log_in(log_in_data)
        while pyautogui.locateCenterOnScreen('role_select_icon.png', region=ROLE_SELECT_ICON_REGION,
                                             confidence=CONFI) is None:
            pass
        get_random_wait(1200, 1500)
        key_2_sent('o')
        while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS,
                                             confidence=CONFI) is None:
            get_random_wait(20000, 30000)
            key_2_sent('o')
            pass

        find_wow_window()


def get_random_wait(low, high):
    # wait for a random time
    time.sleep(random.randint(low * 1000, high * 1000) / 1000000)


RELOAD_SUCCESS = (1036, 709, 180, 50)
OFF_LINE_LOGO_REGION = (10, 30, 250, 150)
BT_LOGGED_IN_REGION = (250, 650, 350, 200)
ROLE_SELECT_ICON_REGION = (550, 650, 250, 100)
acc_f = open("account.txt", "r")
acc_lines = acc_f.readlines()
account_id = acc_lines[0][:-1]
account_psd = acc_lines[1][:-1]
log_in_data = [account_id, account_psd]
bn_target = winshell.shortcut(os.path.join(winshell.desktop(), "暴雪战网.lnk")).path
CONFI = 0.9


# game parameters setup
if os.path.basename(__file__) == 'ptbt_grading_k45v_v2.0.py':
    port = 'COM5'  # note I'm not using Mac OS-X
elif os.path.basename(__file__) == 'ptbt_sur.py':
    port = 'COM3'
else:
    port = ''
    print('Wrong file name found!')
    sys.exit()

if port != '':
    ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2)  # wait for arduino

check_image = {'level23': 'level23.png',
               'level24': 'level24.png',
               'level25': 'level25.png',
               'vs_image': 'vs_image.png',
               'round_end': 'round_end.png',
               'dead_choose': 'dead_choose.png',
               'revival_c_key': 'revival_c_key.png',
               'black_teeth_2': 'black_teeth_2.png',
               'black_teeth_3': 'black_teeth_3.png',
               'rush_3': 'rush_3.png',
               '2nd_pet_feature': '2nd_pet_feature.png',
               '3rd_pet_feature': '3rd_pet_feature.png',
               '1st_pet_feature': '1st_pet_feature.png',
               'black_teeth_buff': 'black_teeth_buff.png',
               '1st_dead_mark': 'dead_mark.png',
               '2nd_dead_mark': 'dead_mark.png',
               '3rd_dead_mark': 'dead_mark.png',
               'up_dead_icon1': 'up_dead_icon.png',
               'up_dead_icon2': 'up_dead_icon.png',
               'up_vacant_icon1': 'up_vacant_icon.png',
               'up_vacant_icon2': 'up_vacant_icon.png',
               'dead_icon_on_pet_menu1': 'dead_icon_on_pet_menu.png',
               'dead_icon_on_pet_menu2': 'dead_icon_on_pet_menu.png',
               'dead_icon_on_pet_menu3': 'dead_icon_on_pet_menu.png'
               }
if os.path.basename(__file__) == 'ptbt.py':
    check_cord = {'level_check_box': (320, 320, 40, 40),
                  'vs_image': (620, 40, 100, 50),
                  'round_end': (600, 640, 100, 100),
                  'dead_choose': (300, 600, 400, 200),
                  'revival_c_key': (270, 650, 50, 50),
                  'black_teeth_2':  (410, 680, 100, 100),
                  'black_teeth_3': (470, 670, 100, 100),
                  'rush_3': (370, 680, 100, 100),
                  '2nd_pet_feature': (470, 670, 100, 100),
                  '3rd_pet_feature': (410, 680, 100, 100),
                  '1st_pet_feature': (470, 670, 100, 100),
                  'black_teeth_buff': (900, 160, 300, 60)
                  }
elif os.path.basename(__file__) == 'ptbt_sur.py':
    check_cord = {'level_check_box': (320, 320, 350, 350),
                  'vs_image': (465, 35, 530, 75),
                  'round_end': (380, 685, 450, 755),
                  'dead_choose': (230, 690, 430, 750),
                  'revival_c_key': (85, 660, 120, 700),
                  'black_teeth_2': (270, 690, 330, 750),
                  'black_teeth_3': (325, 685, 380, 750),
                  'rush_3': (210, 690, 270, 750),
                  '2nd_pet_feature': (325, 685, 380, 750),
                  '3rd_pet_feature': (270, 690, 330, 750),
                  '1st_pet_feature': (325, 685, 380, 750)
                  }
else:
    check_cord = {'level_check_box': (320, 320, 40, 40),
                  'vs_image': (620, 40, 100, 50),
                  'round_end': (600, 640, 100, 100),
                  'dead_choose': (300, 600, 400, 200),
                  'revival_c_key': (270, 650, 50, 50),
                  'black_teeth_2':  (410, 680, 100, 100),
                  'black_teeth_3': (470, 670, 100, 100),
                  'rush_3': (370, 680, 100, 100),
                  '2nd_pet_feature': (470, 670, 100, 100),
                  '3rd_pet_feature': (410, 680, 100, 100),
                  '1st_pet_feature': (470, 670, 100, 100),
                  'black_teeth_buff': (900, 100, 300,220),
                  '1st_dead_mark': (370, 580, 50, 50),
                  '2nd_dead_mark': (560, 580, 50, 50),
                  '3rd_dead_mark': (750, 580, 50, 50),
                  'up_dead_icon1': (170, 35, 50, 50),
                  'up_dead_icon2': (170, 78, 50, 50),
                  'up_vacant_icon1': (170, 35, 50, 50),
                  'up_vacant_icon2': (170, 78, 50, 50),
                  'dead_icon_on_pet_menu1': (305, 240, 40, 40),
                  'dead_icon_on_pet_menu2': (305, 365, 40, 40),
                  'dead_icon_on_pet_menu3': (305, 490, 40, 40)
                  }

battle_action = {1: (2, 1, 3),
                 2: (2, 1, 3),
                 3: (3, 1, 2)
                 }

TIME_ADJ = 0.60
# set wow window to up_left
find_wow_window()

# use ctrl as a start button
print('press ctrl to start')
engine.say('请按CONTROL键开始')
engine.runAndWait()

while not keyboard.is_pressed('ctrl'):
    pass
logging.info('ctrl key was pressed, loop begins!')
engine.say('程序开始！')
engine.runAndWait()
winsound.Beep(500, 300)

# checking the baby level
# baby_level = check_level()
baby_level = 25
# mainloop start
last_revival_time = time.time()
current_pet = 1
is_pets_alive = {1: True,
                 2: True,
                 3: True}

# while baby_level < 26:   # rematch auto up-leveling team
while datetime.now().hour != 4:  # end on 04:00 am
    time.sleep(random.randint(2000, 4000) / 1000)
    # if revival key is ready to do the revival after at least 5 minutes
    if time.time() - last_revival_time >= 480:
        while not is_it_found('revival_c_key'): # not all dead but time is ok for it
            check()
            pass
        key_2_sent('c')
        sleep(500, 900)
        last_revival_time = time.time()

    # loading battle
    battle_loaded = False

    check_pet_alive()

    left_pets = 0
    for i in range(3):
        if is_pets_alive.get(i + 1):
            left_pets += 1
    if left_pets <= 1:
        revival()

    while not battle_loaded:
        ld_battle = load_battle('x')
        if ld_battle is not None:
            battle_loaded = True
        else:
            ld_battle = load_battle('x')
            if ld_battle is not None:
                battle_loaded = True
            else:
                ld_battle = load_battle('z')
                if ld_battle is not None:
                    battle_loaded = True
                else:
                    ld_battle = load_battle('c')
                    if ld_battle is not None:
                        battle_loaded = True
                    else:
                        # wait for revival
                        sleep_time = 480 - (time.time() - last_revival_time) - 10
                        if sleep_time >= 10:
                            logging.info('all dead! sleep ' +
                                         str(sleep_time) + ' seconds to revival.')
                            time.sleep(sleep_time)
                        while not is_it_found('revival_c_key'):
                            check()
                            pass
                        key_2_sent('c')
                        sleep(500, 900)

    # battle loop start
    battle_is_running = True
    logging.info('battle start!')
    sleep(8000 * TIME_ADJ, 9000 * TIME_ADJ)

    battle_time = time.time()

    # count the pets alive
    while battle_is_running:
        left_pets = 0
        for i in range(3):
            if is_pets_alive.get(i + 1):
                left_pets += 1
        print('now there are %d pets left.' % left_pets)
        time.sleep(random.randint(2000, 3000) / 1000)
        pt = pet_check()
        if pt != 0:
            current_pet = pt
        print('current PET = ' + str(current_pet))
        if is_debuffed():
            time.sleep(3)
            key_2_sent(str(battle_action.get(current_pet)[1]))
            sleep(12000 * TIME_ADJ, 13000 * TIME_ADJ)
            result = check_for_attack_result()
            # pets dead round
            if result == 0:
                is_pets_alive[current_pet] = False
                left_pets -= 1
                next_pet = current_pet + 1
                if next_pet > 3:
                    next_pet = 1
                if is_pets_alive.get(next_pet):
                    current_pet = next_pet
                    key_2_sent(str(current_pet))
                    sleep(500, 800)
                    logging.info('bb is dead, change to next one')
                    print('bb is dead, change to next one')
                else:
                    next_pet += 1
                    if next_pet > 3:
                        next_pet = 1
                    if is_pets_alive.get(next_pet):
                        current_pet = next_pet
                        key_2_sent(str(current_pet))
                        sleep(500, 800)
                        logging.info('2 bbs are dead, change to the last one')
                        print('2 bbs are dead, change to the last one')
                    else:
                        set_all_dead()
                        battle_is_running = False
                        print('all bbs dead')
            # battle ended
            elif result == -1:
                current_pet = -1
                print('battle is ended!')
                battle_is_running = False
            # normal ending round
            elif result == 1:
                if left_pets != 1:
                    key_2_sent('4')
                    sleep(5000 * TIME_ADJ, 6000 * TIME_ADJ)
                # now in the pet picking menu
                next_pet = current_pet + 1
                if next_pet > 3:
                    next_pet = 1
                if is_pets_alive.get(next_pet):
                    current_pet = next_pet
                    key_2_sent(str(current_pet))
                    sleep(500, 800)
                    logging.info('change to next one')
                    print('change to next one')
                else:
                    next_pet += 1
                    if next_pet > 3:
                        next_pet = 1
                    if is_pets_alive.get(next_pet):
                        current_pet = next_pet
                        key_2_sent(str(current_pet))
                        sleep(500, 800)
                        logging.info('change to the last one')
                        print('change to the last one')
                    else:
                        sleep(500, 800)
                        key_2_sent('6')
                        set_all_dead()
                        logging.info('the other 2 are dead, fight with this one again')
                        print('the other 2 are dead, fight with this one again')

            elif result == 99:
                is_pets_alive[current_pet] = False
                left_pets -= 1
                pt = pet_check()
                if pt != 0:
                    current_pet = pet_check()
                else:
                    gt = 0
                    for i in range(3):
                        if is_pets_alive.get(i + 1) is True:
                            current_pet = i + 1
                            gt += 1
                    if gt != 1:
                        # something wrong set all pet dead
                        set_all_dead()
                        battle_is_running = False
                        print('some pets counts running wrong!')
                pass

        else:
            if battle_action.get(current_pet) is not None:
                key_2_sent(str(battle_action.get(current_pet)[0]))
                sleep(12000 * TIME_ADJ, 13000 * TIME_ADJ)
                result = check_for_attack_result()
                # pets dead round
                if result == 0:
                    is_pets_alive[current_pet] = False
                    left_pets -= 1
                    next_pet = current_pet + 1
                    if next_pet > 3:
                        next_pet = 1
                    if is_pets_alive.get(next_pet):
                        current_pet = next_pet
                        key_2_sent(str(current_pet))
                        sleep(500, 800)
                        logging.info('bb is dead, change to next one')
                        print('bb is dead, change to next one')
                    else:
                        next_pet += 1
                        if next_pet > 3:
                            next_pet = 1
                        if is_pets_alive.get(next_pet):
                            current_pet = next_pet
                            key_2_sent(str(current_pet))
                            sleep(500, 800)
                            logging.info('2 bbs are dead, change to the last one')
                            print('2 bbs are dead, change to the last one')
                        else:
                            set_all_dead()
                            battle_is_running = False
                            print('all bbs dead')

                # battle ended
                elif result == -1:
                    current_pet = -1
                    print('battle is ended!')
                    battle_is_running = False

                elif result == 1:
                    pass

                elif result == 99:
                    is_pets_alive[current_pet] = False
                    left_pets -= 1
                    pt = pet_check()
                    if pt != 0:
                        current_pet = pet_check()
                    else:
                        gt = 0
                        for i in range(3):
                            if is_pets_alive.get(i + 1) is True:
                                current_pet = i + 1
                                gt += 1
                        if gt != 1:
                            # something wrong set all pet dead
                            set_all_dead()
                            battle_is_running = False
                            print('some pets counts running wrong!')
                pass

        if time.time() - battle_time >= 460:
            logging.info('battle time too long, let us yielding!')
            print('battle time too long, let us yielding!')
            current_pet = -1

        if current_pet == -1:
            battle_is_running = False
            current_pet = 1
            if is_it_found('vs_image'):
                key_2_sent('6')
                sleep(1200 * TIME_ADJ, 1600 * TIME_ADJ)
                key_2_sent('v')
                sleep(14000 * TIME_ADJ, 16000 * TIME_ADJ)
        print(is_pets_alive)

    if is_pets_alive.get(1) is False and is_pets_alive.get(2) is False and is_pets_alive.get(3) is False:  # all dead
        revival()
        # sleep(2000, 3000)
        # baby_level = check_level()
        # logging.info('baby level is now ' + str(baby_level))


# logging.info('baby level up! program end!')

print(datetime.now())
logging.info('time is up! program end!')


# loop unless the win feature shown
