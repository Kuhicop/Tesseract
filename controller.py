import pyautogui
import os
import win32gui
import time
from playsound import playsound
from datetime import date
from threading import Thread
from pynput import keyboard
from tkinter import *

game_name = "FIFA"
started = False
running = False
loop = True
match_stage = "second"
x = 0
y = 0


class WindowMgr:
    # FOCUS GAME
    def __init__ (self):
        self._handle = None

    def find_window(self, class_name, window_name=None):
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        win32gui.SetForegroundWindow(self._handle)


# CREATE KEYS
COMBINATION1 = [
    {keyboard.Key.ctrl, keyboard.Key.home},
    {keyboard.Key.shift, keyboard.Key.home}
    ]
COMBINATION2 = [
    {keyboard.Key.ctrl, keyboard.Key.end},
    {keyboard.Key.shift, keyboard.Key.end}
    ]

current = set()

def execute1():
    print("executed1")
    global running
    running = True


def execute2():
    print("executed2")
    os._exit(1)


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATION1]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATION1):
            execute1()
    if any([key in COMBO for COMBO in COMBINATION2]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATION2):
            execute2()


def on_release(key):
    pass


def listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


threads = list()
lt = Thread(target=listen)
threads.append(lt)
lt.start()


# FOCUS GAME
def winactivate():
    try:
        log("Activating window")
        w = WindowMgr()
        w.find_window_wildcard(".*" + game_name + ".*")
        w.set_foreground()
        log("Window activated")
    except:
        log("WINDOW ACTIVATION FAILED!")
        os._exit(1)


# PARSE IMAGES
def parse():
    try:
        log("Parsing image")
        import parseimgsb
        text = parseimgsb.parse()
        print("Found text: \n" + text)
        log("Image parsed")
        return text
    except:
        log("IMAGE PARSING FAILED!")
        os._exit(1)


# WRITE LOGS
def log(log_text):
    try:
        print(log_text)
        file = open("logs.txt", "a+")
        file.write(str(date.today()) + " " + log_text + "\n")
        file.close()
    except FileNotFoundError:
        file = open("logs.txt", "w+")
        file.write(str(date.today()) + " LOG FILE CREATED" + "\n")
        file.close()
        file = open("logs.txt", "a+")
        file.write(str(date.today()) + " OLD LOGS REMOVED" + "\n")
        file.close()
    except:
        print("WRITING LOGS FAILED!")
        os._exit(1)


# DELETE OLD LOGS
def delete_old_logs():
    try:
        log("REMOVING OLD LOG FILES")
        os.remove("logs.txt")
        log("OLD LOGS REMOVED")
    except FileNotFoundError:
        file = open("logs.txt", "w+")
        file.write(str(date.today()) + " LOG FILE CREATED" + "\n")
        file.close()


# TAKE SCREENSHOT
def take_screenshot():
    log("Taking screenshot")
    # delete old image
    try:
        os.remove("image.png")
    except FileNotFoundError:
        pass

    pyautogui.screenshot('image.png')

    log("Screenshot saved")


# PRINT BASIC INFO
def console(lbltext):
    # CREATE CONSOLE
    window = Tk()
    window.overrideredirect(1)
    window.wm_attributes("-topmost", 1)
    window.title("Welcome")
    lbl = Label(window, text=lbltext)
    lbl.config(font=("arial", 10))
    lbl.grid(column=0, row=0)
    window.mainloop()


# SPAWN CONSOLE
threads = list()
t = Thread(target=console, args=("Shift+End close \n Shift+Home start",))
threads.append(t)
t.start()


# test screen image
def image_find(img_name):
    try:
        global x
        global y
        x, y = pyautogui.locateCenterOnScreen(img_name + ".png", confidence=0.8)
        print(str(x) + " " + str(y))
        return True
    except TypeError:
        print(img_name + " not found")
        return False


# <-------- SCRIPT START ---

# delete old logs
os.chdir("images")
delete_old_logs()

# activate game window
winactivate()

# take screenshot
take_screenshot()

# detect AFK status
status = parse()
os._exit(1)

while loop:
    while running:
        # take screenshot
        take_screenshot()

        # detect AFK status
        status = parse()

        if "PULSA" in status:
            log("AFK detected")
            log("ClickAFK")
            pyautogui.press("enter")
            log("ClickAFK done")

        # Match starting
        if "EL REGRESO" in status:
            log("EL REGRESO found")
            pyautogui.moveTo(459, 480)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        if "OBJETIVOS INICIALES" in status:
            log("OBJETIVOS INICIALES found")
            pyautogui.moveTo(639, 266)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        if "EQUIPO DE LA SEMANA" in status:
            log("EQUIPO DE LA SEMANA found")
            pyautogui.moveTo(571, 771)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        if "HISTORIAL TEMPORADA" in status:
            log("HISTORIAL TEMPORADA found")
            pyautogui.moveTo(333, 384)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        if "Tu plantilla puede jugar el partido" in status:
            log("Team is ready to play")
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        if "ELEGIR LADO" in status:
            log("Selecting side")
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            while not image_find("go"):
                time.sleep(0.1)
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

        if "ESC PARA JUGAR" in status:
            log("Skipping minigame")
            pyautogui.moveTo(949, 914)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            match_stage = "first"
            i = 0
            while not image_find("go"):
                log("Waiting first time: " + str(i))
                pyautogui.moveTo(1503, 391)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                time.sleep(1)
                i = i + 1
            if image_find("go"):
                match_stage = "go"
                while not "REANUDAR" in status:
                    take_screenshot()
                    status = parse()
                    if image_find("go"):
                        pyautogui.moveTo(x, y)
                        pyautogui.mouseDown()
                        pyautogui.mouseUp()
                pyautogui.moveTo(1112, 367)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                match_stage = "second"

        i = 0
        while "second" in match_stage:
            while not image_find("go"):
                log("Waiting second time: " + str(i))
                pyautogui.moveTo(1503, 391)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                time.sleep(1)
                i = i + 1
            take_screenshot()
            status = parse()
            while not "Partidos restantes" in status:
                if image_find("go"):
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
            match_stage = "none"

        if "Tiros a puerta" in status:
            if "quit" in match_stage:
                log("Exit match")
                pyautogui.moveTo(356, 376)
                pyautogui.mouseDown()
                pyautogui.mouseUp()
                time.sleep(1)
                match_stage = "go"

        if not "ANCUCS" in status:
            if "go" in match_stage:
                if image_find("go"):
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    log("Restart done")
        else:
            log("Fix players")
            playsound("alert.mp3")
            os._exit(1)

        log("loop end")

        # EXIT LOOP
        # running = False
    time.sleep(0.1)

game_name = "TESSERACT"
winactivate()
os._exit(1)
# ------------------------->
