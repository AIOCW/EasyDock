from tools_function import save_app_icon

from entity.app_info import AppInfo

from setting import Setting

from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QMenu, QAction
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QRect

import win32com.client

from default_config import *

TAG = "father_q_label.py="


class FatherQLabel(QLabel):
    def __init__(self, tips, main_window, main_window_centralWidget):
        super().__init__(tips, main_window_centralWidget)
        self.main_window = main_window
        self.show_left = True

        # drag in
        self.setAcceptDrops(True)
        self.socket_thread = main_window.socket_thread

        # right clicked
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略

        # double click
        self.is_close = False
        self.mouseDoubleClickEvent(self)

    def rightMenuShow(self, pos):  # 添加右键菜单
        menu = QMenu(self)
        menu.addAction(QAction('设置', menu))
        menu.addAction(QAction('动作2', menu))
        menu.addAction(QAction('动作3', menu))
        menu.triggered.connect(self.menuSlot)
        menu.exec_(QCursor.pos())

    def menuSlot(self, act):
        print(act.text())
        if act.text() == '设置':
            print(TAG)
            self.main_window.setting.show()

    # drag in
    def dragEnterEvent(self, QDragEnterEvent):  # 3
        print('Drag Enter')
        if QDragEnterEvent.mimeData().hasText():
            QDragEnterEvent.acceptProposedAction()

    def dragMoveEvent(self, QDragMoveEvent):  # 4
        # pass
        print('Drag Move')

    def dragLeaveEvent(self, QDragLeaveEvent):  # 5
        # pass
        print('Drag Leave')

    # 重写父类
    def dropEvent(self, QDropEvent):  # 6
        print('Drag Drop')
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
        else:
            app_name = app_target.split('.lnk')[0]
        self.socket_thread.get_other_client_data(txt_path)
        # self.socket_thread.send_file(txt_path, '1000')

    def mouseDoubleClickEvent(self, *args, **kwargs):
        if self.is_close:
            self.main_window.main_window.resize(5 + input_window_width + 5, window_height)
            self.main_window.app_list_widget.setGeometry(
                QRect(0, 0, 0, 0))
            self.main_window.message_label.setGeometry(0, 0, 0, 0)
            self.setGeometry(5, 2, input_window_width, input_window_height)
            self.is_close = False
        else:
            # self.main_window.main_layout.addWidget(self.main_window.app_list_widget)
            if len(self.main_window.app_info_dict) == 0:
                self.main_window.main_window.resize(5 + message_window_width + 5 + input_window_width + 5 + icon_width + 5, window_height)
                self.main_window.app_list_widget.setGeometry(
                    QRect(5 + message_window_width + 5 + input_window_width + 5, 2, icon_width,
                          icon_height))
            else:
                if self.show_left:
                    self.main_window.main_window.resize(5 + message_window_width + 5 + input_window_width + 5 + icon_width * len(self.main_window.app_info_dict) + 5, window_height)
                    self.main_window.app_list_widget.setGeometry(
                        QRect(5 + message_window_width + 5 + input_window_width + 5, 2, icon_width * len(self.main_window.app_info_dict),
                              icon_height))
                    self.setGeometry(QRect(5 + message_window_width + 5, 2, input_window_width, input_window_height))
                    self.main_window.message_label.setGeometry(QRect(5, 2, message_window_width, message_window_height))
                else:
                    self.main_window.main_window.resize(5 + input_window_width + 5 + icon_width * len(self.main_window.app_info_dict) + 5, window_height)
                    self.main_window.app_list_widget.setGeometry(
                        QRect(5 + input_window_width + 5, 2, icon_width * len(self.main_window.app_info_dict),
                              icon_height))
                    self.setGeometry(QRect(5, 2, input_window_width, input_window_height))
                    self.main_window.message_label.setGeometry(QRect(0, 0, 0, 0))
            self.is_close = True
        print("{} double click".format(TAG))
