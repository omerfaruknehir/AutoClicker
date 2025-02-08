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
import subprocess
from ctypes import windll

if getattr(sys, 'frozen', True):
    application_path = sys.executable
elif __file__:
    application_path = __file__
else:
    raise FileNotFoundException("Application not found")

application_dir = os.path.dirname(application_path)

hwnd = win32gui.GetForegroundWindow()
USER_NAME = getpass.getuser()

exit = sys.exit

def cmd(command):
    return subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True)

def quit(e=True):
    if os.path.exists(os.path.join(application_dir, '.lock')):
        os.remove(os.path.join(application_dir, '.lock'))
    if e:
        exit()

def _add_to_startup(file_path=""):
    if file_path == "":
        file_path = application_path
    bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME
    target = bat_path + '\\' + "AutoClicker.lnk"
    if os.path.exists(target):
        os.remove(target)
    out = "AutoClicker.lnk"
    shell = wincl.Dispatch('WScript.Shell', USER_NAME)
    shortcut = shell.CreateShortcut(out)
    shortcut.Targetpath = f'"{application_path}"'
    shortcut.Arguments = '--run'
    #shortcut.IconLocation = os.path.dirname(os.path.realpath(__file__)) + '\\icon.ico'
    shortcut.Save()
    #shutil.move(out, r'C:\Users\%s\d4h238qfuehygwor34q987twhvumvru3gyferughf33785erugh934fo.lnk' % USER_NAME)
    cmd(f"move \"{out}\" \"{target}\"")
    return target

def _add_to_programs():
    bat_path = r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" % USER_NAME
    target = bat_path + '\\' + "AutoClicker.lnk"
    if os.path.exists(target):
        os.remove(target)
    out = "AutoClicker.lnk"
    shell = wincl.Dispatch('WScript.Shell', USER_NAME)
    shortcut = shell.CreateShortcut(out)
    shortcut.Targetpath = f'"{application_path}"'
    shortcut.Arguments = '--run'
    #shortcut.IconLocation = os.path.dirname(os.path.realpath(__file__)) + '\\icon.ico'
    shortcut.Save()
    #shutil.move(out, r'C:\Users\%s\d4h238qfuehygwor34q987twhvumvru3gyferughf33785erugh934foje.lnk' % USER_NAME)
    cmd(f"move \"{out}\" \"{target}\"")
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
    if os.path.exists((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" % USER_NAME) + '\\' + "AutoClicker.lnk"):
        os.remove((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" % USER_NAME) + '\\' + "AutoClicker.lnk")

def reinstall():
    startup = os.path.exists((r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME) + '\\' + "AutoClicker.lnk")
    uninstall()
    install()
    if startup:
        add_to_startup()

def set_cps(cps):
    with open(os.path.join(application_dir, '.conf'), 'w') as f:
        f.write(str(cps))

def get_cps():
    if not os.path.exists(os.path.join(application_dir, '.conf')):
        set_cps(default_cps)
        return default_cps
    with open(os.path.join(application_dir, '.conf'), 'r') as f:
        return int(f.read())

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

    target_cps = get_cps()

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
    x = msvcrt.getch().lower()
    if x == b'k':
        with open(os.path.join(os.path.dirname(__file__), '.lock'), 'rb') as lockfile:
            try:
                os.kill(int.from_bytes(lockfile.read(), byteorder='big'), signal.SIGTERM)
            except Exception as e:
                print("An unexpected exception occured, please report it! (And run again))")
                print(e)
                quit()
        os.remove(os.path.join(os.path.dirname(__file__), '.lock'))
    else:
        exit()

try:
    with open(os.path.join(os.path.dirname(__file__), '.lock'), 'wb') as lockfile:
        lockfile.write(os.getpid().to_bytes(3, byteorder='big'))

    helptext = f"""AutoClicker by Ömer Faruk Nehir (https://github.com/OFN01)
    [ --help        -h ]:  Show this message and exit.
    [ --addstartup  -s ]:  Add program to startup as user.
    [ --rmstartup   -S ]:  Remove program from startup.
    [ --install     -i ]:  Install this program as user (Still needs this python file and contents).
    [ --uninstall   -u ]:  Uninstall this program from system and remove from startup.
    [ --reinstall   -R ]:  Uninstall and installs this program to fix errors.
    [ --resetcps    -C ]:  Resets cps (clicks per second) number to default ({default_cps}).
    [ --cps         -c ]:  Writes or sets (with -c={{cps}} or --cps={{cps}}) cps of AutoClicker.
    [ --run         -r ]:  Run the AutoClicker."""

    for arg in sys.argv[1:]:
        if arg in ['--help', '-h', '/h', '/help']:
            print(helptext)
        elif arg in ['--addstartup', '-s']:
            add_to_startup()
            print('Added to startup successfully')
        elif arg in ['--rmstartup', '-S']:
            remove_from_startup()
            print('Removed from startup')
        elif arg in ['--install', '-i']:
            install()
            print('Installed successfully')
        elif arg in ['--uninstall', '-u']:
            uninstall()
            print('Uninstalled successfully')
        elif arg in ['--reinstall', '-R']:
            reinstall()
            print('Reinstalled successfully')
        elif arg in ['-cps', '-c']:
            print('current cps is', get_cps())
        elif arg in ['-resetcps', '-C']:
            fr = get_cps()
            set_cps(default_cps)
            print(f'cps resetted from {fr} to {default_cps}')
        elif arg.startswith('--cps=') and (arg.removeprefix('--cps=').isnumeric() or arg.removeprefix('--cps=') == 'default'):
            fr = get_cps()
            set_cps(default_cps if arg.removeprefix('--cps=') == 'default' else arg.removeprefix('--cps='))
            print(f'cps set from {fr} to', default_cps if arg.removeprefix('--cps=') == 'default' else arg.removeprefix('--cps='))
        elif arg.startswith('-c=') and (arg.removeprefix('-c=').isnumeric() or arg.removeprefix('-c=') == 'default'):
            fr = get_cps()
            set_cps(default_cps if arg.removeprefix('-c=') == 'default' else arg.removeprefix('-c='))
            print(f'cps set from {fr} to', default_cps if arg.removeprefix('-c=') == 'default' else arg.removeprefix('-c='))
        elif arg in ['--run', '-r']:
            pass
        else:
            print(f'Unknown option: {arg}\nUse -h for more information.')

    if len(sys.argv) == 1 or ('--run' in sys.argv[1:] or '-r' in sys.argv[1:]):
        main()
except KeyboardInterrupt:
    print('\nUser Quit')
    quit()
except Exception as e:
    quit(False)
    raise e
quit()