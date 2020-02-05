

class AppInfo(object):
    id = 0
    name = ""
    path = ""
    icon_path = ""
    icon_gray_path = ""

    def __init__(self, id, name, path, icon_path, icon_gray_path):
        self.id = id
        self.name = name
        self.path = path
        self.icon_path = icon_path
        self.icon_gray_path = icon_gray_path


if __name__ == "__main__":
    app_info = AppInfo(1, "Chrome", "C:/e.exe", "C:/e.ico", "C:/e_gray.exe")
    print(app_info.id)




