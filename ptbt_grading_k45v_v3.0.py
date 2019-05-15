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

from bt_log_in import *

# y is the start battle key
# P is for pet setting window
# z search the pet boss
# x search the the mob
# c revival key
# v for confirmation button   /click StaticPopup1Button1
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


def is_off_line():
    start_t = time.time()
    found = None
    while time.time() - start_t <= 6:
        found = pyautogui.locateCenterOnScreen('off_line_logo.png', region=OFF_LINE_LOGO_REGION,
                                               grayscale=False, confidence=0.9)
        if found is not None:
            engine.say('掉线，重新连接')
            engine.runAndWait()
            break
    return found


def pet_check():
    if is_it_found('2nd_pet_feature'):
        if debug_voice:
            engine.say('当前是二号宠物')
            engine.runAndWait()
        return 2
    elif is_it_found('2nd_pet_feature_beta'):
        if debug_voice:
            engine.say('当前是二号宠物')
            engine.runAndWait()
        return 2
    elif is_it_found('3rd_pet_feature'):
        if debug_voice:
            engine.say('当前是三号宠物')
            engine.runAndWait()
        return 3
    elif is_it_found('1st_pet_feature'):
        if debug_voice:
            engine.say('当前是一号宠物')
            engine.runAndWait()
        return 1
    else:
        if debug_voice:
            engine.say('当前宠物未知')
            engine.runAndWait()
        return 0


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
                if debug_voice:
                    engine.say('剩余三个，回合结束')
                    engine.runAndWait()
                return 1
            elif is_it_found('dead_choose'):
                if debug_voice:
                    engine.say('剩余三个，宠物死亡，重新选择宠物')
                    engine.runAndWait()
                return 0
            elif not is_it_found('vs_image'):
                if debug_voice:
                    engine.say('剩余三个，对战结束')
                    engine.runAndWait()
                return -1
        elif left_pets == 2:
            if is_it_found('up_dead_icon1'):
                if debug_voice:
                    engine.say('剩余两个，现在死亡一个，结束战斗')
                    engine.runAndWait()
                return 99  # dead don't have to choose
            elif is_it_found('round_end'):
                if debug_voice:
                    engine.say('剩余两个，回合结束')
                    engine.runAndWait()
                return 1
            elif not is_it_found('vs_image'):
                if debug_voice:
                    engine.say('剩余两个，结束对战')
                    engine.runAndWait()
                return -1
        elif left_pets == 1:
            if is_it_found('round_end'):
                if debug_voice:
                    engine.say('剩余一个，回合结束')
                    engine.runAndWait()
                return 1
            elif not is_it_found('vs_image'):
                if debug_voice:
                    engine.say('剩余一个，结束对战')
                    engine.runAndWait()
                return -1
            elif time.time() - tm >= 6:
                if debug_voice:
                    engine.say('大于六秒，无法判断,默认回合结束')
                    engine.runAndWait()
                return 1
        if time.time() - tm >= 15: # in case some trick to prevent from swift team member
            if debug_voice:
                engine.say('大于十秒，无法判断,默认回合结束')
                engine.runAndWait()
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
        if debug_voice:
            engine.say('黑齿')
            engine.runAndWait()
        return True
    else:
        print('target is not debuffed')
        if debug_voice:
            engine.say('无黑齿')
            engine.runAndWait()
        return False


def sleep(millisecond1, millisecond2):
    tm = random.uniform(millisecond1, millisecond2) / 1000  # a ture float random wait
    print('wait for ' + str(tm) + ' seconds....')
    time.sleep(tm)
    return


def load_battle(enemy):
    key_2_sent(enemy)
    sleep(300, 400)
    key_2_sent('y')  # y is the start battle key
    end = time.time() + 3.5 * 1
    fd = None
    while time.time() < end:
        fd = is_it_found('vs_image')
        if fd is not None:
            break
        key_2_sent('y')
        sleep(1000, 1200)
    return fd


def find_wow_window():
    while True:
        hwndwow = win32gui.FindWindow(None, '魔兽世界')
        if hwndwow != 0:
            hwndwowrec = win32gui.GetWindowRect(hwndwow)
            print(hwndwow, hwndwowrec)
            win32gui.MoveWindow(hwndwow, 0, 0, 1296, 759, 0)
            logging.info('wow window was set to the up left corner')
            break
    return


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
        if debug_voice:
            engine.say('等待复活')
            engine.runAndWait()
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
            done_received = True
        else:
            ard.flush()
            time.sleep(0.3)
    return


def check(is_forced=False):
    if is_forced or is_off_line() is not None:
        kill_process('Wow.exe', '魔兽世界')
        time.sleep(10)
        log_in(account_data, bn_target, '魔兽世界')
        while pyautogui.locateCenterOnScreen('role_select_icon.png', region=ROLE_SELECT_ICON_REGION,
                                             confidence=CONFI) is None:
            pass
        sleep(1200, 1500)
        key_2_sent('o')
        while pyautogui.locateCenterOnScreen('reload_success.png', region=RELOAD_SUCCESS,
                                             confidence=CONFI) is None:
            sleep(20000, 30000)
            key_2_sent('o')
            pass
        find_wow_window()


RELOAD_SUCCESS = (1036, 709, 180, 50)
OFF_LINE_LOGO_REGION = (10, 30, 250, 150)
BT_LOGGED_IN_REGION = (250, 650, 350, 200)
ROLE_SELECT_ICON_REGION = (550, 650, 250, 100)
acc_f = open("account.txt", "r")
acc_lines = acc_f.readlines()
account_id = acc_lines[0][:-1]
account_psd = acc_lines[1][:-1]
account_data = [account_id, account_psd]
bn_target = winshell.shortcut(os.path.join(winshell.desktop(), "暴雪战网.lnk")).path
CONFI = 0.9


# game parameters setup
port = 'COM9'  # note I'm not using Mac OS-X

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
               '2nd_pet_feature_beta': 'bite_cooling.png',
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
               'dead_icon_on_pet_menu3': 'dead_icon_on_pet_menu.png',
               'rush_cooling': 'rush_cooling.png',
               'rush_ok': 'rush_ok.png',
               'bite_cooling': 'bite_cooling.png'
               }

check_cord = {'level_check_box': (320, 320, 40, 40),
              'vs_image': (620, 40, 100, 50),
              'round_end': (600, 640, 100, 100),
              'dead_choose': (300, 600, 400, 200),
              'revival_c_key': (270, 650, 50, 50),
              'black_teeth_2':  (410, 680, 100, 100),
              'black_teeth_3': (470, 670, 100, 100),
              '2nd_pet_feature': (470, 670, 100, 100),
              '2nd_pet_feature_beta': (470, 670, 100, 100),
              '3rd_pet_feature': (410, 680, 100, 100),
              '1st_pet_feature': (470, 670, 100, 100),
              'rush_cooling': (350, 670, 100, 100),
              'rush_ok': (350, 670, 100, 100),
              'bite_cooling': (470, 670, 100, 100),
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
engine.say('请按a启动魔兽，或按b跳过启动')
engine.runAndWait()

while True:
    if keyboard.is_pressed('a'):
        engine.say('启动魔兽中')
        engine.runAndWait()
        check(True)
        break
    elif keyboard.is_pressed('b'):
        # set wow window to up_left
        find_wow_window()
        break

# use ctrl as a start button
print('press ctrl to start')
engine.say('请按CONTROL键开始')
engine.runAndWait()
debug_voice = False

# ====================================================================================================
while not keyboard.is_pressed('ctrl'):
    pass
logging.info('ctrl key was pressed, loop begins!')
engine.say('程序开始！')
engine.runAndWait()
winsound.Beep(500, 300)


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
    key_2_sent('k')

    left_pets = 0
    for i in range(3):
        if is_pets_alive.get(i + 1):
            left_pets += 1
    if left_pets <= 1:
        engine.say('只有一个宠物是活的，等待复活')
        revival()
    if debug_voice:
        speech = '现有' + str(left_pets) + '个活的宠物'
        engine.say(speech)
        engine.runAndWait()
    if left_pets == 2:
        start_pets = 2
    else:
        start_pets = 3

    while not battle_loaded:
        ld_battle = load_battle('x')
        if ld_battle is not None:
            battle_loaded = True
            engine.say('找到泽地小歌手')
            engine.runAndWait()
        else:
            ld_battle = load_battle('x')
            if ld_battle is not None:
                battle_loaded = True
                engine.say('找到泽地小歌手')
                engine.runAndWait()
            else:
                ld_battle = load_battle('z')
                if ld_battle is not None:
                    battle_loaded = True
                    engine.say('找到小艺')
                    engine.runAndWait()
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

        # check current pet
        # check how many pet left before begin
        # check how many are dead now
        # first debuffed
        # if rush is availalbe rush
        # if rush is not available, to he rest action

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
            if is_it_found('rush_ok'):
                if debug_voice:
                    engine.say('可以冲锋')
                    engine.runAndWait()
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
                        if start_pets == 2:
                            sent_pet_key = current_pet -1
                        else:
                            sent_pet_key = current_pet
                        key_2_sent(str(sent_pet_key))
                        sleep(500, 800)
                        logging.info('bb is dead, change to next one')
                        print('bb is dead, change to next one')
                    else:
                        next_pet += 1
                        if next_pet > 3:
                            next_pet = 1
                        if is_pets_alive.get(next_pet):
                            current_pet = next_pet
                            if start_pets == 2:
                                sent_pet_key = current_pet - 1
                            else:
                                sent_pet_key = current_pet
                            key_2_sent(str(sent_pet_key))
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
                        if start_pets == 2:
                            sent_pet_key = current_pet -1
                        else:
                            sent_pet_key = current_pet
                        key_2_sent(str(sent_pet_key))
                        sleep(500, 800)
                        logging.info('change to next one')
                        print('change to next one')
                    else:
                        next_pet += 1
                        if next_pet > 3:
                            next_pet = 1
                        if is_pets_alive.get(next_pet):
                            current_pet = next_pet
                            if start_pets == 2:
                                sent_pet_key = current_pet - 1
                            else:
                                sent_pet_key = current_pet
                            key_2_sent(str(sent_pet_key))
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
            elif not is_it_found('bite_cooling') or current_pet != 2:
                if debug_voice:
                    engine.say('不可冲锋')
                    engine.runAndWait()
                key_2_sent(str(battle_action.get(current_pet)[2]))
            else:
                key_2_sent(str(battle_action.get(current_pet)[0]))
                if debug_voice:
                    engine.say('攻击技能全部冷却中')
                    engine.runAndWait()

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
                        if start_pets == 2:
                            sent_pet_key = current_pet -1
                        else:
                            sent_pet_key = current_pet
                        key_2_sent(str(sent_pet_key))
                        sleep(500, 800)
                        logging.info('bb is dead, change to next one')
                        print('bb is dead, change to next one')
                    else:
                        next_pet += 1
                        if next_pet > 3:
                            next_pet = 1
                        if is_pets_alive.get(next_pet):
                            current_pet = next_pet
                            if start_pets == 2:
                                sent_pet_key = current_pet - 1
                            else:
                                sent_pet_key = current_pet
                            key_2_sent(str(sent_pet_key))
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
                sleep(1200 , 1600 )
                key_2_sent('v')
                sleep(14000 * TIME_ADJ, 16000 * TIME_ADJ)
        print(is_pets_alive)

    if is_pets_alive.get(1) is False and is_pets_alive.get(2) is False and is_pets_alive.get(3) is False:  # all dead
        revival()



# logging.info('baby level up! program end!')

print(datetime.now())
logging.info('time is up! program end!')


# loop unless the win feature shown

