import win32process

def get_handle(app_info):
    return win32process.CreateProcess(app_info.path, '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None,
                               win32process.STARTUPINFO())