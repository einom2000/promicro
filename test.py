import serial, keyboard
import time, random
import logging, json

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


port = 'COM10' # note I'm using Mac OS-X
ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2) # wait for Arduino
check_image = {}
# main loop
script_running = True
while script_running:
    last_revival_time = time.time()
    # check if all the team members are alive, if not, wait for a revival
    # check if the baby's level is less than 24, if not, change to a next baby
    # cast macro to get the target
    # react with the target
    # wait and check the pbattle feature shown
    # battle loop start
    # loop unless the win feature shown