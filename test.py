import bluetooth
import sys
bd_addr = "a3:3a:11:04:0d:5d" #itade address

port = 4
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))
print('Connected')
sock.settimeout(1.0)
sock.send("x")
print('Sent data')

data = sock.recv(1)
print('received [%s]'%data)

sock.close()