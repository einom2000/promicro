import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
from datetime import datetime

# P is for pet setting window
# F1 search the pet boss
# F2 search the the mob
# F3 revival key
# level of the first baby (329,328)(340,340)
# vs image (627, 44)(668, 69)
# round_end image (544, 695) (582, 736)
# dead_choose image (399, 697)(558, 733)
# revival button image (642, 71)(677, 109))
#  1,4,2,2,1,2,4,3,1,3,4,2,...
# add keyboard.release(all) in arduino

logging.basicConfig(filename='leveling.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )
logging.info('Program starts!')


def is_round_end():
    fd = pyautogui.locateOnScreen(check_image.get('round_end'),
                                  region=check_cord.get('round_end'))
    return fd

def is_revivaled(last_time):
    if time.time() - last_time >= 480:
        key_2_sent('f3')
        time.sleep(random.randint(3, 5) / 10)
        return True


def load_battle(enemy):
    key_2_sent(enemy)
    time.sleep(random.randint(5, 9) / 10)
    key_2_sent('y')  # y is the start battle key
    time.sleep(random.randint(15, 20) / 10)
    end_time = time.time() + 60 * 1
    fd = None
    while time.time() < end_time:
        fd = pyautogui.locateOnScreen(check_image.get('vs_image'),
                                      region=check_cord.get('vs_image'))
        if fd is not None:
            break
    return fd


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
    fd = pyautogui.locateCenterOnScreen(level_img,
                                        region=position)
    return fd


def key_2_sent(key):
    key_sent = str(key)
    ard.flush()
    print ("Python value sent: " + key_sent)
    ard.write(str.encode(key_sent))
    time.sleep(0.5) # I shortened this to match the new value in your Arduino code
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


# game parameters setup
port = 'COM10'  # note I'm using Mac OS-X
ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2) # wait for Arduino
check_image = {'level23': 'level23.png',
               'level24': 'level24.png',
               'level25': 'level25.png',
               'vs_image': 'vs_image.png',
               'round_end': 'round_end.png',
               'dead_choose': 'dead_choose.png',
               'revival': 'revival.png'
               }
check_cord = {'level_check_box': (320, 320, 350, 350),
              'vs_image': (620, 40, 680, 80),
              'round_end': (530, 710, 600, 750),
              'dead_choose': (370, 680, 580, 750)
              }

battle_action = (1, 4, 2, 2, 1, 2, 4, 3, 1, 3, 4, 2)

# set wow window to up_left
find_wow_window()

# use ctrl as a start button
print('press ctrl to start')
while not keyboard.is_pressed('ctrl'):
    pass
logging.info('ctrl key was pressed, loop begins!')

# checking the baby level
baby_level = 0
key_2_sent('p')  # p is the pet info short_key
for i in range(23, 26):
    if found_level(check_image.get('level' + str(i)),
                   check_cord.get('level_check_box')) is not None:
        baby_level = i
        break
logging.info("checking: baby level is " + str(baby_level))
time.sleep(random.randint(5, 7) / 10)
key_2_sent('p')  # to close pet info window

# mainloop start
last_revival_time = time.time()
while baby_level < 25:
    # every 8 minutes to do the revival
    if is_revivaled(last_revival_time):
        last_revival_time = time.time()

    #loading battle
    battle_loaded = False
    while not battle_loaded:
        ld_battle = load_battle('f2')
        if ld_battle is not None:
            battle_loaded = True
        else:
            ld_battle = load_battle('f1')
            if ld_battle is not None:
                battle_loaded = True
            else:
                # wait for revival
                sleep_time = 480 - (time.time() - last_revival_time)
                if sleep_time >= 10:
                    logging.info('all dead! sleep ' +
                                 str(sleep_time) + ' seconds to revival.')
                    time.sleep(sleep_time)
                while not is_revivaled(last_revival_time):
                    pass

    # battle loop start
    battle_is_running = True
    logging.info('battle start!')
    i = 0
    case = 0
    while battle_is_running:
        key_2_sent(str(battle_action[i]))
        time.sleep(random.randint(8, 12) / 10)
        end_time = time.time() + 60
        while time.time() <= end_time:
            if is_round_end():
                case = 1
                break
            if is_dead_choose:
                case = 2
                break
            if not vs_image:
                case = 3
                break
        case1:
        case2:
        case3:




# loop unless the win feature shown