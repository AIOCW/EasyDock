from tools_function import save_app_icon

from entity.app_info import AppInfo
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QMenu, QAction
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt

import win32com.client



class FatherQListWidgetItem(QListWidgetItem):
    def __init__(self):
        super().__init__()