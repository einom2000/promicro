import pyautogui
import keyboard, time, win32api, win32gui

last_position = (0, 0)
while True:
    if keyboard.is_pressed('\\\\') and last_position != pyautogui.position():
        print(pyautogui.position())
        last_position = pyautogui.position()

# import datetime
# now = datetime.datetime.now().hour
# while now != 9:
#     print(now)

# while not keyboard.is_pressed('ctrl'):
#     pass
#
# hwnd = win32gui.FindWindow(None, '魔兽世界')
# print(hwnd)
# print(win32gui.GetWindowRect(hwnd))