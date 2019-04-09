import pyautogui
import time
import keyboard

while True:
    if keyboard.is_pressed(' '):
        print(pyautogui.position())
        time.sleep(3)