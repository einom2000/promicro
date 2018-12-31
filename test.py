import serial, keyboard
import time

#The following line is for serial over GPIO
port = 'COM10' # note I'm using Mac OS-X

ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2) # wait for Arduino

def key_2_sent(key):
    key_2_sent = str(key)
    ard.flush()
    print ("Python value sent: " + key_2_sent)
    ard.write(str.encode(key_2_sent))
    time.sleep(0.5) # I shortened this to match the new value in your Arduino code
    # wating for promicro to send 'Done'
    done_received = False
    while not done_received:
        original_msg = str(ard.read(ard.inWaiting())) # read all characters in buffer
        msg = original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
        print(msg[0:4])
        if msg[0:4] == 'Done':
            print ("Message from arduino: ")
            print (msg)
            done_received = True
        else:
            ard.flush()
            time.sleep(0.3)
    return

# while not keyboard.is_pressed('ctrl'):
#     pass
# time.sleep(1)
# for i in "abcdefghijklmnopqrstuvWXYZ!":
#     key_2_sent(i)

