import win32process
import os

if __name__ == "__main__":
    os.chdir("D:\portable_softeware\EasyDock")
    handle = win32process.CreateProcess("dock_main.exe", '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO())