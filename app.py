# Shift+F11 to hide and show console
# Shift+F12 to stop and start autoclick
# Use mouse side buttons to use left and right autoclick

default_cps = 20

from pyWinhook import cpyHook, HookConstants, HookManager, GetKeyState
import win32com.client as wincl
import threading
import time
import pythoncom
import getpass
import os
import shutil
import win32gui
import sys
import signal
import msvcrt

hwnd = win32gui.GetForegroundWindow()
USER_NAME = getpass.getuser()

def quit():
    os.remove(os.path.join(os.path.dirname(__file__), '.lock'))

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

def reinstall():
    uninstall()
    install()

hiding = False
running = False
pressing1 = False
pressing2 = False

def main():
    import win32api, win32con

    #win32gui.ShowWindow(hwnd , win32con.SW_HIDE)

    print("Press Shift+F11 to hide or show the window")
    print("Press Shift+F12 to stop or start AutoClicker")

    #def lclick(down=True):
    #    x, y = win32api.GetCursorPos()
    #    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    #    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    #def rclick():
    #    x, y = win32api.GetCursorPos()
    #    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    #    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

    def t():
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

        def keyboard_handler(event):
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
            return event.IsTransition() or not event.IsInjected()

        try:
            cph = HookManager()
            #cph.KeyDown = keyboard_handler
            cph.SubscribeKeyDown(keyboard_handler)
            cph.HookKeyboard()
            cpyHook.cSetHook(HookConstants.WH_MOUSE_LL, mouse_handler)
            #cpyHook.cSetHook(HookConstants.WH_KEYBOARD, keyboard_handler)
            pythoncom.PumpMessages() # Loop
        finally:
            pass
            cpyHook.cUnhook(HookConstants.WH_MOUSE_LL)
            cpyHook.cUnhook(HookConstants.WH_KEYBOARD)

    if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf')):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'w') as f:
            f.write(str(default_cps))

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'r') as f:
        target_cps = int(f.read())

    thethread = threading.Thread(target=t, daemon=True)
    thethread.start()

    timer = time.time()
    wait = 1 / target_cps
    error = 0
    while True:
        global running
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
        while time.time() - timer < (wait - error)/2:
            pass
        now = time.time()
        if pl:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        if pr:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
        while now - timer < wait - error:
            now = time.time()

        error += (now - timer) - wait
        timer = now

if os.path.exists(os.path.join(os.path.dirname(__file__), '.lock')):
    print("Another instance is already running. Please kill the running process continue by pressing 'k' or press any key to close this window.")
    if msvcrt.getch().lower() == 'k':
        with open(os.path.join(os.path.dirname(__file__), '.lock'), 'rb') as lockfile:
            os.kill(int.from_bytes(lockfile.read(), byteorder='big'), signal.SIGTERM)
        os.remove(os.path.join(os.path.dirname(__file__), '.lock'))
    else:
        exit()

try:
    with open(os.path.join(os.path.dirname(__file__), '.lock'), 'wb') as lockfile:
        lockfile.write(os.getpid().to_bytes(3, byteorder='big'))

    helptext = f"""AutoClicker by Ömer Faruk Nehir (https://github.com/OFN01)
    [ --help       , -h ]: Show this message and exit.
    [ --addstartup , -S ]: Add program to startup as user.
    [ --rmstartup  , -s ]: Remove program from startup.
    [ --install    , -i ]: Install this program as user (Still needs this python file and contents).
    [ --uninstall  , -u ]: Uninstall this program from system and remove from startup.
    [ --reinstall  , -R ]: Uninstall and installs this program to fix errors.
    [ --resetcps   , -C ]: Resets cps (clicks per second) number to default ({default_cps}).
    [ --cps        , -c ]: Writes or sets (with -c={{cps}} or --cps={{cps}}) cps of AutoClicker.
    [ --run        , -r ]: Run the AutoClicker."""

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
        elif arg in ['--reinstall', '-R']:
            reinstall()
        elif arg in ['-cps', '-c']:
            if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf')):
                with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'w') as f:
                    f.write(str(default_cps))
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'r') as f:
                print('current cps is', f.read())
        elif arg in ['-cps', '-c']:
            if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf')):
                with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'w') as f:
                    f.write(str(default_cps))
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'r') as f:
                print('current cps is', f.read())
        elif arg in ['-resetcps', '-C']:
            if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf')):
                with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'w') as f:
                    f.write(str(default_cps))
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'r') as f:
                fr = f.read()
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'w') as f:
                f.write(str(default_cps))
            print(f'cps resetted from {fr} to {default_cps}')
        elif arg.startswith('--cps=') and (arg.removeprefix('--cps=').isnumeric() or arg.removeprefix('--cps=') == 'default'):
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'w') as f:
                f.write(str(default_cps) if arg.removeprefix('--cps=') == 'default' else arg.removeprefix('--cps='))
                print('cps set as', default_cps if arg.removeprefix('--cps=') == 'default' else arg.removeprefix('--cps='))
        elif arg.startswith('-c=') and (arg.removeprefix('-c=').isnumeric() or arg.removeprefix('-c=') == 'default'):
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.conf'), 'w') as f:
                f.write(default_cps if arg.removeprefix('-c=') == 'default' else arg.removeprefix('-c='))
                print('cps set as', default_cps if arg.removeprefix('-c=') == 'default' else arg.removeprefix('-c='))
        elif arg in ['--run', '-r']:
            pass
        else:
            print(f'Unknown option: {arg}\nUse -h for more information.')

    if len(sys.argv) == 1 or ('--run' in sys.argv[1:] or '-r' in sys.argv[1:]):
        main()
except KeyboardInterrupt:
    print('\nUser Quit')
    quit()