import pyautogui
import time,random
import keyboard
import pyperclip
import serial
from datetime import datetime



def sleep(millisecond1, millisecond2):
    tm = random.uniform(millisecond1, millisecond2) / 1000  # a ture float random wait
    print('wait for ' + str(tm) + ' seconds....')
    time.sleep(tm)
    return



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


# print(datetime.now().hour)
port = 'COM9'  # com5 for kv45

ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2)  # wait for arduino
gossip = ('一一一一一一一一',
          '二恶热热热热热热热',
          '四恩凯利金融联考',
          '三三三',
          '呜呜呜'
          '六六六',
          '七七七',
          '八八八',
          '九九九',
          '是是是是',
          '上课就拉开',
          '可哎呀啊',
          '二二二二二二二二二' )
gossip_length = len(gossip)
while True:
    if keyboard.is_pressed(' '):
        key_2_sent('m')
        pyperclip.copy(gossip[random.randrange(gossip_length)])
        sleep(400, 600)
        key_2_sent('>')
        time.sleep(2)
        key_2_sent('o')

# # left_pets =3
# print('now there are %d pets left.' % left_pets)

# while True:
#     if keyboard.is_pressed(' '):
#         break
#
# for i in range(3000):
#     pyautogui.press('f')
#     time.sleep(random.randint(50000, 80000) / 100000)
#     if keyboard.is_pressed(' '):
#         break

