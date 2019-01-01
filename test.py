import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
from datetime import datetime

# P is for pet setting window
# z search the pet boss
# x search the the mob
# c revival key
# level of the first baby (329,328)(340,340)
# vs image (627, 44)(668, 69)
# round_end image (544, 695) (582, 736)
# dead_choose image (399, 697)(558, 733)
# revival button image (642, 71)(677, 109))
# revival c key button image (274, 657) (299, 687)
# black_teeth_2.png (432, 685)(481, 737)
# black_teeth_3.png (490, 687) (535, 734)
# rush_3.png (373, 687) (419, 735)
#  1,4,2,2,1,2,4,3,1,3,4,2,...
# add keyboard.release(all) in arduino

logging.basicConfig(filename='leveling.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )
logging.info('Program starts!')


def is_it_found(key):
    fd = pyautogui.locateOnScreen(check_image.get(key),
                                  region=check_cord.get(key))
    return fd


def sleep(millisecond1, millisecond2):
    time.sleep(random.randint(millisecond1 // 10, millisecond2 // 10) / 100)
    return


def load_battle(enemy):
    key_2_sent(enemy)
    sleep(500, 900)
    key_2_sent('y')  # y is the start battle key
    sleep(1500, 2000)
    end = time.time() + 60 * 1
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


# game parameters setup
port = 'COM10'  # note I'm using Mac OS-X
ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2) # wait for arduino

check_image = {'level23': 'level23.png',
               'level24': 'level24.png',
               'level25': 'level25.png',
               'vs_image': 'vs_image.png',
               'round_end': 'round_end.png',
               'dead_choose': 'dead_choose.png',
               'revival_c_key': 'revival_c_key.png',
               'black_teeth_2': 'black_teeth_2.png',
               'black_teeth_3': 'black_teeth_3.png',
               'rush_3': 'rush_3.png'
               }
check_cord = {'level_check_box': (320, 320, 350, 350),
              'vs_image': (620, 40, 680, 80),
              'round_end': (530, 710, 600, 750),
              'dead_choose': (370, 680, 580, 750),
              'revival_c_key': (270, 650, 300, 690),
              'black_teeth_2':  (430, 685, 480, 740),
              'black_teeth_3': (490, 685, 535, 740),
              'rush_3': (370, 680, 420, 735)
              }
battle_action = {1: (1, 0),
                 2: (2, 1),
                 3: (3, 1)
                 }

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
sleep(500, 700)
key_2_sent('p')  # to close pet info window
sleep(600, 900)

# mainloop start
last_revival_time = time.time()
while baby_level < 25:
    # if revival key is ready to do the revival after at least 5 minutes
    if time.time() - last_revival_time >= 400 and is_it_found('revival_c_key'):
        key_2_sent('c')
        sleep(500, 900)
        last_revival_time = time.time()

    #loading battle
    battle_loaded = False
    while not battle_loaded:
        ld_battle = load_battle('x')
        if ld_battle is not None:
            battle_loaded = True
        else:
            ld_battle = load_battle('z')
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
                    pass
                key_2_sent('c')
                sleep(500, 900)


    # battle loop start
    battle_is_running = True
    logging.info('battle start!')
    pets_lives = {1:'alive',
                  2:'alive',
                  3:'alive'}
    current_pet = 1
    while battle_is_running:
        if current_pet == 1:
            key_2_sent(str(battle_action.get(1)[0]))
            while not is_it_found('round_end'):
                pass
            key_2_sent('4')
            sleep(200, 500)
            # now in the pet picking menu
            logging.info('from 1st pet to 2nd pet')
            key_2_sent('2')
            current_pet = 2
            sleep(400, 600)
            if not is_it_found('black_teeth_2'):
                logging.info('pick 2nd pet failed try 3rd pet')
                pets_lives[2] = 'dead'
                key_2_sent('3')
                current_pet = 3
                sleep(400, 600)
                if not is_it_found('black_teeth_3'):
                    logging.info('only 1st pet available back to 1st')
                    pets_lives[3] = 'dead'
                    key_2_sent('1')
                    current_pet = 0
                    sleep(300, 500)

        if current_pet == 2 and pets_lives.get(2) == 'alive'\
                and is_it_found('vs_image'):
            key_2_sent('2')




# loop unless the win feature shown