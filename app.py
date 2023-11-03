# Shift+F11 to hide and show console
# Shift+F12 to stop and start autoclick
# Use mouse side buttons to use left and right autoclick

from pyWinhook import cpyHook, HookConstants, HookManager, GetKeyState
import win32com.client as wincl
import threading
import time
import pythoncom
import ctypes
import getpass
import os
import shutil
import win32gui
import sys

hwnd = win32gui.GetForegroundWindow()
USER_NAME = getpass.getuser()

def _add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "AutoClicker.bat", "w") as bat_file:
        bat_file.write(r'python "%s"' % file_path)

def _add_to_programs():
    bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" % USER_NAME
    target = bat_path + '\\' + "AutoClicker.lnk"
    if os.path.exists(target):
        os.remove(target)
    out = "AutoClicker.lnk"
    shell = wincl.Dispatch('WScript.Shell', USER_NAME)
    shortcut = shell.CreateShortcut(out)
    shortcut.Targetpath = r'C:\Users\omerf\AppData\Local\Microsoft\WindowsApps\python.exe'
    shortcut.Arguments = f'"{os.path.realpath(__file__)}"'
    shortcut.IconLocation = os.path.dirname(os.path.realpath(__file__)) + '\\icon.ico'
    shortcut.Save()
    shutil.move(out, r'C:\Users\%s\d4h238qfuehygwor34q987twhvumvru3gyferughf33785erugh934foje.lnk' % USER_NAME)
    os.system(f"move \"C:\\Users\\%s\\d4h238qfuehygwor34q987twhvumvru3gyferughf33785erugh934foje.lnk\" \"{target}\"" % USER_NAME)
    return target

def add_to_startup():
    if not os.path.exists((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME) + '\\' + "AutoClicker.lnk"):
        _add_to_startup()

def remove_from_startup():
    if os.path.exists((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME) + '\\' + "AutoClicker.lnk"):
        os.remove((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME) + '\\' + "AutoClicker.lnk")

def install():
    _add_to_programs()

def uninstall():
    remove_from_startup()
    if os.path.exists((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME) + '\\' + "AutoClicker.lnk"):
        os.remove((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME) + '\\' + "AutoClicker.lnk")

def main():
    import win32api, win32con

    hiding = True
    win32gui.ShowWindow(hwnd , win32con.SW_HIDE)

    user32 = ctypes.windll.user32

    def lclick(down=True):
        x, y = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


    def rclick():
        x, y = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

    running = False
    pressing1 = False
    pressing2 = False


    def t():
        XBUTTON1 = 0x0001
        XBUTTON2 = 0x0002

        wm = {
            0x020B: "WM_XBUTTONDOWN",
            0x020C: "WM_XBUTTONUP",
            0x0201: "WM_LBUTTONDOWN",
        }

        def mouse_handler(msg, x, y, data, flags, time, hwnd, window_name):
            name = wm.get(msg, None)
            if name and running:
                xb = data >> 16
                global pressing1
                global pressing2
                if name == "WM_XBUTTONDOWN":
                    if xb == 1:
                        pressing1 = True
                    elif xb == 2:
                        pressing2 = True
                    return False
                if name == "WM_XBUTTONUP":
                    if xb == 1:
                        pressing1 = False
                    elif xb == 2:
                        pressing2 = False
                    return False
                # if name == "WM_LBUTTONDOWN":
                #    user32.PostQuitMessage(0)
            return True

        def OnKeyboardEvent(event):
            if event.KeyID == 123 and GetKeyState(HookConstants.VKeyToID('VK_RSHIFT')) == 128: # SHIFT F-12
                global running
                print('Stopped' if running else 'Running')
                running = not running
                return False
            if event.KeyID == 122 and GetKeyState(HookConstants.VKeyToID('VK_RSHIFT')) == 128: # SHIFT F-11
                global hiding
                if hiding:
                    win32gui.ShowWindow(hwnd , win32con.SW_SHOW)
                else:
                    win32gui.ShowWindow(hwnd , win32con.SW_HIDE)
                hiding = not hiding
                return False
            return True

        try:
            hm = HookManager()
            hm.KeyDown = OnKeyboardEvent
            hm.HookKeyboard()
            cpyHook.cSetHook(HookConstants.WH_MOUSE_LL, mouse_handler)
            pythoncom.PumpMessages() # Loop
        finally:
            cpyHook.cUnhook(HookConstants.WH_MOUSE_LL)

    try:
        with open(os.path.join(os.path.abspath(os.path.dirname(__name__), '.conf')), 'r') as f:
            target_cps = int(f.read())  # Change this to set cps what you want

        thethread = threading.Thread(target=t, daemon=True)
        thethread.start()

        timer = time.time()
        wait = 1 / target_cps
        error = 0
        while True:
            if not running:
                timer = time.time()
                time.sleep(0.5)
                continue
            if  not (pressing1 or pressing2):
                time.sleep(0.01)
                continue
            try:
                x, y = win32api.GetCursorPos()
            except:
                running = False
                print('Stopped (Due to error like you are writing passwords, etc.)')
                continue
            pl = pressing1
            pr = pressing2
            if pl:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            if pr:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
            while time.time() - timer < ((1 / target_cps) - error)/2:
                pass
            now = time.time()
            if pl:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            if pr:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
            while now - timer < (1 / target_cps) - error:
                now = time.time()

            error += (now - timer) - (1 / target_cps)
            timer = now
    except KeyboardInterrupt:
        print('\nQuit')
        user32.PostQuitMessage(0)
    quit()

helptext = """AutoClicker by Ömer Faruk Nehir (https://github.com/OFN01)
[ --help       , -h       ]: Show this message and exit
[ --addstartup , -S       ]: Add program to startup as user
[ --rmstartup  , -s       ]: Remove program from startup
[ --install    , -i       ]: Install this program as user (Still needs this python file and contents)
[ --uninstall  , -u       ]: Uninstall this program from system and remove from startup
[ --cps={cps}  , -c={cps} ]: Set clicks per second of AutoClicker"""

for arg in sys.argv[1:]:
    if arg in ['--help', '-h', '/h', '/help']:
        print(helptext)
    elif arg in ['--addstartup', '-S']:
        add_to_startup()
    elif arg in ['--rmstartup', '-s']:
        remove_from_startup()
    elif arg in ['--install', '-i']:
        install()
    elif arg in ['--uninstall', '-u']:
        uninstall()
    elif arg.startswith('--cps=') and arg.removeprefix('--cps=').isnumeric():
        with open(os.path.join(os.path.abspath(os.path.dirname(__name__), '.conf')), 'w') as f:
            f.write(arg.removeprefix('--cps='))
    elif arg.startswith('-c=') and arg.removeprefix('-c=').isnumeric():
        with open(os.path.join(os.path.abspath(os.path.dirname(__name__), '.conf')), 'w') as f:
            f.write(arg.removeprefix('-c='))
    else:
        print(f'Unknown option: {arg}\nUse -h for more information.')

if len(sys.argv) == 1 or '--run' in sys.argv[1:]:
    main()