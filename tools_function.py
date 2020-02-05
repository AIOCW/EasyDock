import win32ui
import win32gui
from PIL import Image
import winreg


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def save_app_icon(app_path, save_path, save_gray_path):
    large, small = win32gui.ExtractIconEx(app_path, 0)
    win32gui.DestroyIcon(small[0])
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 32, 32)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), large[0])
    bmpstr = hbmp.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGBA',
        (32, 32),
        bmpstr, 'raw', 'BGRA', 0, 1
    )
    img.save(save_path)
    img = img.convert("LA")
    img.save(save_gray_path)


if __name__ == "__main__":
    save_app_icon("C:\Program Files (x86)\TeamViewer\TeamViewer.exe", "appIcon/TeamViewer_gray.png", "appIcon/TeamViewer_gray.png")