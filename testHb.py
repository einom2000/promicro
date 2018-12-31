import pyautogui
import keyboard,time

last_position = (0, 0)
while True:
    if keyboard.is_pressed('ctrl') and last_position != pyautogui.position():
        print(pyautogui.position())
        last_position = pyautogui.position()


