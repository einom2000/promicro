import pyautogui
import time,random
import keyboard

# while True:
#     if keyboard.is_pressed(' '):
#         print(pyautogui.position())
#         time.sleep(3)
# left_pets =3
# print('now there are %d pets left.' % left_pets)

while True:
    if keyboard.is_pressed(' '):
        break

for i in range(3000):
    pyautogui.press('f')
    time.sleep(random.randint(50000, 80000) / 100000)
    if keyboard.is_pressed(' '):
        break