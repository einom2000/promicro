import serial
import time

#The following line is for serial over GPIO
port = 'COM9' # note I'm using Mac OS-X


ard = serial.Serial(port, 9600, timeout=5)
time.sleep(2) # wait for Arduino

i = 0

while (i < 50):
    # Serial write section

    setTempCar1 = 63
    setTempCar2 = 37
    ard.flush()
    setTemp1 = str(setTempCar1)
    setTemp2 = str(setTempCar2)
    print ("Python value sent: ")
    print (setTemp1)
    ard.flushInput()
    ard.flushOutput()
    ard.write(str.encode(setTemp1))
    time.sleep(1) # I shortened this to match the new value in your Arduino code

    # Serial read section
    original_msg = str(ard.read(ard.inWaiting())) # read all characters in buffer
    msg =original_msg.replace('b\'', '').replace('\\r\\n', "   ")[:-2]
    print ("Message from arduino: ")
    print (msg)
    i = i + 1
else:
    serial.Serial(port, 9600).close()
    print("Exiting")
