# !/bin/env python
#
# From: earl@microcontrollerelectonics.com
#

import serial, sys, glob, select

dev = "/dev/ttyACM*"
scan = glob.glob(dev)
rate = "115200"

if len(scan) == 0:
    dev = '/dev/ttyUSB*'
    scan = glob.glob(dev)
    if len(scan) == 0:
        print("Unable to find any ports scanning for /dev/[ttyACM*|ttyUSB*]" + dev)
        sys.exit()

serport = scan[0]

if len(sys.argv) > 1:
    l = len(sys.argv) - 1
    while l > 0:
        if sys.argv[l][0] == '/':
            serport = sys.argv[l]
        else:
            rate = sys.argv[l]
        l = l - 1

ser = serial.Serial(port=serport, baudrate=rate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS, timeout=1)
print("connected to: " + ser.portstr)

while True:
    try:
        line = ser.readline()
        if line:
            # Uncomment the next line to display the input from the serial port in hex format
            #     for x in line: print ("%s") % (x.encode('hex')),
            print(line),
    except KeyboardInterrupt:
        sys.exit()
    except:
        pass
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        line = line.replace("\n", "\r\n")
        # Uncomment the next two lines to display the typed in characters in hex format
        #    for x in line: print ("%s") % (x.encode('hex')),
        #    print
        ser.write(line)

ser.close()
sys.exit()

