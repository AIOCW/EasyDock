from tools_function import save_app_icon
from default_config import *

from entity.app_info import AppInfo
from dao.app_info_dao import insert, delete

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu, QAction
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QSize, QRect

import win32com.client
import win32process
import win32event

from father_q_list_widget_item import FatherQListWidgetItem


class FatherQListWidget(QListWidget):
    def __init__(self, main_window, centralWidget):
        super().__init__(centralWidget)
        # drag in
        self.setAcceptDrops(True)
        self.main_window = main_window

        # right clicked
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略

    # drag in
    def dragEnterEvent(self, QDragEnterEvent):  # 3
        # print('Drag Enter')
        if QDragEnterEvent.mimeData().hasText():
            QDragEnterEvent.acceptProposedAction()

    def dragMoveEvent(self, QDragMoveEvent):  # 4
        pass
        # print('Drag Move')

    def dragLeaveEvent(self, QDragLeaveEvent):  # 5
        pass
        # print('Drag Leave')

    # 重写父类
    def dropEvent(self, QDropEvent):  # 6
        # print('Drag Drop')
        # MacOS
        # txt_path = QDropEvent.mimeData().text().replace('file:///', '/')

        # Linux
        # txt_path = QDropEvent.mimeData().text().replace('file:///', '/').strip()

        # Windows
        txt_path = QDropEvent.mimeData().text().replace('file:///', '')
        print(txt_path)
        app_target = txt_path.split('/')[-1]
        if '.exe' in app_target:
            app_name = app_target.split('.exe')[0]
            app_path = txt_path
            app_icon_gray_path = "appIcon/" + app_name + "_gray.png"
            app_icon_path = "appIcon/" + app_name + ".png"

        else:
            app_name = app_target.split('.lnk')[0]
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(txt_path)
            app_path = shortcut.Targetpath
            app_icon_gray_path = "appIcon/" + app_name + "_gray.png"
            app_icon_path = "appIcon/" + app_name + ".png"

        print(app_path)
        if app_name in self.main_window.app_info_dict:
            print("error")
            return
        save_app_icon(app_path, app_icon_path, app_icon_gray_path)

        app_info = AppInfo(len(self.main_window.app_info_dict), app_name, app_path, app_icon_path, app_icon_gray_path)
        self.main_window.app_info_dict[app_name] = app_info
        insert(app_info)
        item = FatherQListWidgetItem()
        item.setSizeHint(QSize(icon_width, icon_height))
        item.setWhatsThis(app_name)
        print(item.whatsThis())
        if self.main_window.app_setting.use_rgb:
            item.setIcon(QIcon(app_icon_path))
        else:
            item.setIcon(QIcon(app_icon_gray_path))

        self.main_window.app_list_widget.addItem(item)
        self.main_window.app_list_widget.setGeometry(
            QRect(5 + message_window_width + 5 + input_window_width + 5, 2, icon_width * len(self.main_window.app_info_dict),
                  icon_height))
        self.main_window.main_window.resize(5 + message_window_width + 5 + input_window_width + 5 + icon_width * len(
            self.main_window.app_info_dict) + 5, window_height)


    def rightMenuShow(self, pos):  # 添加右键菜单
        menu = QMenu(self)
        # menu.addAction(QAction('强制退出', menu))
        menu.addAction(QAction('删除', menu))
        menu.triggered.connect(self.menuSlot)
        menu.exec_(QCursor.pos())

    def menuSlot(self, act):
        if act.text() == "删除":
            name = self.currentItem().whatsThis()
            print(name, self.currentRow())
            self.takeItem(self.currentRow())
            delete(self.main_window.app_info_dict[name].id)
            self.main_window.app_info_dict.pop(name)
            self.main_window.app_list_widget.setGeometry(
                QRect(5 + message_window_width + 5 + input_window_width + 5, 2, icon_width * len(self.main_window.app_info_dict),
                      icon_height))
            self.main_window.main_window.resize(
                5 + message_window_width + 5 + input_window_width + 5 + icon_width * len(
                    self.main_window.app_info_dict) + 5, window_height)