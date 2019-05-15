import win32gui
import time
import win32api
import random
import pyautogui
import psutil
import sys
import pyttsx3

engine = pyttsx3.init()

class LoginWindow:

    windowHwnd = 0

    def __init__(self, programdir, windowname, username, userpwd):
        self.programDir = programdir
        self.windowName = windowname
        self.userName = username
        self.userPwd = userpwd


    def runbnet(self):
        exist = win32gui.FindWindow(None, self.windowName)
        if exist == 0:
            win32api.WinExec(self.programDir)
        return

    def findWindow(self):
        while True:
            hwndbnt = win32gui.FindWindow(None, self.windowName)
            if hwndbnt == 0:
                continue
            else:
                win32gui.MoveWindow(hwndbnt, 100, 100, 365, 541, True)
                pyautogui.moveTo(150, 150)
                pyautogui.click()
                print(hwndbnt)
                print(self.windowName)
            break
        time.sleep(1)
        win32gui.SetForegroundWindow(hwndbnt)
        time.sleep(1)
        return hwndbnt

    def login(self):
        # to log in id
        pyautogui.keyDown('shift')
        time.sleep(0.1)
        pyautogui.press('tab')
        time.sleep(0.123)
        pyautogui.keyUp('shift')
        time.sleep(random.randint(3, 5) / 10)
        # clear box
        pyautogui.press('backspace')
        time.sleep(random.randint(3, 5) / 10)
        # change to english
        pyautogui.press('shift')
        time.sleep(random.randint(3, 5) / 10)
        win32api.LoadKeyboardLayout('00000409', 1)
        time.sleep(random.randint(3, 5) / 10)
        # typein
        pyautogui.typewrite(self.userName, interval=(random.randint(15, 30) / 100))
        time.sleep((random.randint(15, 30) / 100))
        pyautogui.press('tab')
        pyautogui.typewrite(self.userPwd, interval=(random.randint(15, 30) / 100))
        time.sleep(5)
        for i in range(3):
            pyautogui.press('tab')
            time.sleep(random.randint(3, 5) / 10)
        # log in
        pyautogui.press('enter')
        return


def log_in(account, bn_target, target_game):
    BT_LOGGED_IN_REGION = (250, 650, 350, 200)
    # open in battle net login window
    loginbt = LoginWindow(bn_target, '暴雪战网登录', account[0], account[1])
    logged_in = False
    logging_time = time.time()
    bt_window = 0
    while not logged_in:
        loginbt.runbnet()
        bn_hwnd = loginbt.findWindow()
        loginbt.login()
        # wait for the battle net window shows up
        time_login = time.time()
        while time.time() - time_login <= 50:
            bt_window = win32gui.FindWindow(None, '暴雪战网')
            if bt_window > 0:
                logged_in = True
                break
        if not logged_in:
            kill_process('Battle.net.exe', '暴雪战网登录')
        if time.time() - logging_time >= 600:
            # after 10 minutes failure, terminate program
            sys.exit()
    win32gui.SetForegroundWindow(bt_window)
    win32gui.MoveWindow(bt_window, 0, 0, 1280, 820, 1)
    bt_rec = win32gui.GetWindowRect(bt_window)

    time.sleep(1)

    while True:
        found = pyautogui.locateCenterOnScreen('bt_logged_in.png', region=BT_LOGGED_IN_REGION,
                                               grayscale=False, confidence=0.8)
        if found is not None:
            x = found[0]
            y = found[1]
            break
    pyautogui.moveTo(x, y, 1,  pyautogui.easeInQuad)
    pyautogui.click(x, y)

    # waiting for wow running
    wow_is_running = False
    wow_window = 0
    while not wow_is_running:
        wow_window = win32gui.FindWindow(None, target_game)
        if wow_window > 0:
            wow_is_running = True

    time.sleep(20)
    win32gui.EnumWindows(enumhandler,target_game)


def kill_process(process_name, wd_name):
    if win32gui.FindWindow(None, wd_name):
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == process_name:
                proc.kill()
                break
    return


def enumhandler(hwnd, lParam):
    # enumwindows' callback function
    # if found move to up_left corner
    if win32gui.IsWindowVisible(hwnd):
        if lParam in win32gui.GetWindowText(hwnd):
            # rect = win32gui.GetWindowRect(hwnd)
            # print(rect[2] - rect[0], rect[3] - rect[1])
            win32gui.MoveWindow(hwnd, 0, 0, 1296, 759, True)
            txt = '找到'+ lParam + '窗口'
            engine.say(txt)
            engine.runAndWait()


if __name__ == "__main__":
    pass
