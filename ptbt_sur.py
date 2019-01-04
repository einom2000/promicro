import serial, keyboard, sys
import win32api, win32gui, winsound
import time, random, pyautogui
import logging, json
import cv2, os
from datetime import datetime

# P is for pet setting window
# z search the pet boss
# x search the the mob
# c revival key
# v for confirmation button
# level of the first baby (329,328)(340,340)
# vs image (627, 44)(668, 69)
# round_end image (544, 695) (582, 736)
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


def pet_check():
    if is_it_found('2nd_pet_feature'):
        return 2
    elif is_it_found('3rd_pet_feature'):
        return 3
    else:
        return 1


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


def check_for_attack_result():
    tm = time.time()
    while True:
        if is_it_found('round_end'):
            return 1
        elif is_it_found('dead_choose'):
            return 0
        elif not is_it_found('vs_image'):
            return -1
        if time.time() - tm >= 15:  # in case some trick to prevent from swift team member
            return 1


def is_it_found(key):
    fd = pyautogui.locateOnScreen(check_image.get(key),
                                  region=check_cord.get(key),
                                  grayscale=False,
                                  confidence=0.9)
    print(key, fd)
    return fd


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
    end = time.time() + 20 * 1
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
            if os.path.basename(__file__) == 'ptbt_sur.py':
                win32gui.MoveWindow(hwndwow, 0, 0, 988, 768, 0)
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


def master_action(pet_num):
    sleep(300, 500)
    next_pet_num = pet_num % 2 * (-1) + 3
    if pets_lives.get(pet_num) == 'alive' and pet_check() == pet_num:
        key_2_sent(str(battle_action.get(pet_num)[0]))
        sleep(8000, 9000)
        result = check_for_attack_result()
        print('current pet = ' + str(pet_num))
        print('result= ' + str(result))
        if result == 0:
            logging.info('No. ' + str(pet_num) + ' pet was killed!')
            pets_lives[pet_num] = 'dead'
            if pets_lives.get(next_pet_num) == 'alive':
                key_2_sent(str(next_pet_num))  # change to 3rd or 2nd pet
                pet_num = next_pet_num
                sleep(7000, 8000)
            else:
                key_2_sent('6')  # yield
                sleep(1200, 1600)
                key_2_sent('v')
                logging.info('both 2nd and 3rd were killed, yielding')
                sleep(2000, 3000)
                pet_num = -1
        elif result == -1:
            sleep(2000, 3000)
            pet_num = -1
        elif result == 1:
            sleep(2000, 3000)
            if is_it_found('rush_3'):
                key_2_sent(str(battle_action.get(pet_num)[1]))
            else:
                key_2_sent(str(battle_action.get(pet_num)[2]))
            sleep(13000, 15000)
            result = check_for_attack_result()
            if result == 0:
                logging.info('No. ' + str(pet_num) + ' pet was killed!')
                pets_lives[pet_num] = 'dead'
                if pets_lives.get(next_pet_num) == 'alive':
                    key_2_sent(str(next_pet_num))  # change to 3rd pet
                    pet_num = next_pet_num
                    sleep(7000, 8000)
                else:
                    key_2_sent('6')  # yield
                    sleep(1200, 1600)
                    key_2_sent('v')
                    logging.info('both 2nd and 3rd were killed, yielding')
                    sleep(2000, 3000)
                    pet_num = -1
            elif result == -1:
                sleep(2000, 3000)
                pet_num = -1
            elif result == 1:
                key_2_sent('4')
                sleep(5000, 6000)
                if pets_lives.get(next_pet_num) == 'alive':
                    key_2_sent(str(next_pet_num))
                    pet_num = next_pet_num
                    sleep(7000, 8000)
                elif pets_lives.get(1) == 'alive':
                    key_2_sent('1')
                    pet_num = 1
                    sleep(7000, 8000)
    return pet_num


# game parameters setup
if os.path.basename(__file__) == 'ptbt.py':
    port = 'COM10'  # note I'm not using Mac OS-X
elif os.path.basename(__file__) == 'ptbt_sur.py':
    port = 'COM3'
else:
    port = ''
    print('Wrong file name found!')
    sys.exit()

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
               '3rd_pet_feature': '3rd_pet_feature.png'
               }
if os.path.basename(__file__) == 'ptbt.py':
    check_cord = {'level_check_box': (320, 320, 350, 350),
                  'vs_image': (620, 40, 680, 80),
                  'round_end': (530, 680, 600, 750),
                  'dead_choose': (300, 600, 610, 760),
                  'revival_c_key': (270, 650, 300, 690),
                  'black_teeth_2':  (410, 680, 490, 750),
                  'black_teeth_3': (470, 670, 550, 760),
                  'rush_3': (370, 680, 420, 735),
                  '2nd_pet_feature': (470, 670, 550, 760),
                  '3rd_pet_feature': (410, 680, 490, 750)
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
                  '3rd_pet_feature': (270, 690, 330, 750)
                  }
else:
    check_cord = {}
    print('Wrong file name found!')
    sys.exit()


battle_action = {1: (1, 0),
                 2: (2, 1, 3),
                 3: (3, 1, 2)
                 }

# set wow window to up_left
find_wow_window()

# use ctrl as a start button
print('press ctrl to start')
while not keyboard.is_pressed('ctrl'):
    pass
logging.info('ctrl key was pressed, loop begins!')
winsound.Beep(500, 300)

# checking the baby level
baby_level = check_level()

# mainloop start
last_revival_time = time.time()

# while baby_level < 26:   # rematch auto up-leveling team
while datetime.now().hour != 2:  # end on 02:00 am

    current_pet = 1

    # if revival key is ready to do the revival after at least 5 minutes
    if time.time() - last_revival_time >= 420:
        while not is_it_found('revival_c_key'): # not all dead but time is ok for it
            pass
        key_2_sent('c')
        sleep(500, 900)
        last_revival_time = time.time()

    # loading battle
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
    sleep(8000, 9000)
    pets_lives = {1: 'alive',
                  2: 'alive',
                  3: 'alive'}

    battle_time = time.time()

    while battle_is_running:
        if current_pet == 1 and pets_lives.get(1) == 'alive' and pet_check() == 1:
            key_2_sent(str(battle_action.get(1)[0]))
            sleep(8000, 9000)
            result = check_for_attack_result()
            print('current pet = ' + str(current_pet))
            print('result= ' + str(result))
            if result == 0:
                key_2_sent('6')
                sleep(500, 800)
                logging.info('bb is dead')
                key_2_sent('v')      # yield
                sleep(2000, 3000)
                current_pet = -1
                battle_is_running = False
            elif result == -1:
                current_pet = -1
                battle_is_running = False
            elif result == 1:
                key_2_sent('4')
                sleep(5000, 6000)
                # now in the pet picking menu
                logging.info('from 1st pet to 2nd pet')
                last_pet = current_pet
                key_2_sent('2')
                current_pet = 2
                sleep(7000, 8000)
                if not is_it_found('black_teeth_2'):
                    logging.info('pick 2nd pet failed try 3rd pet')
                    pets_lives[2] = 'dead'
                    key_2_sent('3')
                    last_pet = current_pet
                    current_pet = 3
                    sleep(7000, 8000)
                    if not is_it_found('black_teeth_3'):
                        logging.info('only 1st pet available back to 1st')
                        pets_lives[3] = 'dead'
                        while is_it_found('vs_image'):
                            key_2_sent('1')
                            sleep(7000, 8000)
                        current_pet = -1
                        battle_is_running = False

        if current_pet == 1 and pet_check() != 1:
            pets_lives[1] = 'dead'
            current_pet = pet_check()
        # if the assumed pet is not the deck pet, then it is believed dead, and change the assumed pet to the
        # deck pet.
        if current_pet == 2:
            current_pet = master_action(2)

        if current_pet == 3:
            current_pet = master_action(3)

        if time.time() - battle_time >= 460:
            logging.info('battle time too long, let us yielding!')
            print('battle time too long, let us yielding!')
            current_pet = -1

        if current_pet == -1:
            battle_is_running = False
            current_pet = 1
            if is_it_found('vs_image'):
                key_2_sent('6')
                sleep(1200, 1600)
                key_2_sent('v')
                sleep(14000, 16000)

        current_pet = pet_check()
        pets_lives[current_pet] = 'alive'

    if pets_lives.get(1) == 'dead' or pets_lives.get(2) == 'dead' or pets_lives.get(3) == 'dead':  # all dead
        while not is_it_found('revival_c_key'):
            pass
        key_2_sent('c')
        logging.info('revivaled all.')
        sleep(2000, 3000)
        last_revival_time = time.time()
        current_pet = 1
        sleep(2000, 3000)
        baby_level = check_level()
        logging.info('baby level is now ' + str(baby_level))


# logging.info('baby level up! program end!')

logging.info('time is up! program end!')








# loop unless the win feature shown