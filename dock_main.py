import fix_qt_import_error
import sys
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QGridLayout, QComboBox

import win32process
import json

from setting import Setting

from father_q_main_window import FatherQMainWindow
from father_q_list_widget import FatherQListWidget
from father_q_label import FatherQLabel
from father_q_list_widget_item import FatherQListWidgetItem

from entity.app_info import AppInfo
from dao.app_info_dao import insert, delete, select

from entity.app_setting import AppSetting
from data_manager.app_setting_location import init_setting, select_setting, update_setting

from default_config import *

from data_manager.common_tools import init_table_data_for_setting

from tools_socket_client import SocketQThread

TAG = "dock_main:    "


class DockMain(object):
    app_info_dict = {}
    app_run_info_dict = {}

    def setupUi(self, MainWindow):
        self.main_window = MainWindow
        self.main_window.setObjectName("main_window")
        self.centralWidget = QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")
        self.main_window.setCentralWidget(self.centralWidget)

        # init_table_data_for_setting()

        self.init_config()

        self.init_thead()

        self.init_data()
        self.init_ui()

    def init_config(self):
        # init_table_data_for_setting()
        self.app_setting = select_setting()

    def init_thead(self):
        self.socket_thread = SocketQThread(self.app_setting)
        self.socket_thread.my_signal.connect(self.set_self_message)
        self.socket_thread.start()

    def init_data(self):
        for app_info in select():
            self.app_info_dict[app_info.name] = app_info

    def init_ui(self):
        desktop = QApplication.desktop()
        self.main_window.move(desktop.width() * 0.4, 0)
        self.main_window.setWindowTitle("Ass")
        self.main_window.setWindowIcon(QIcon("images/icon.png"))
        # https://www.easyicon.net/1188455-Fingerprint_icon.html
        self.main_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.Tool)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # dialog.setWindowFlags(QtCore.Qt.Widget)  # 取消置顶
        self.main_window.setWindowOpacity(0.8)  # 设置窗口透明度
        self.main_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.main_window.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.app_list_widget = FatherQListWidget(self, self.centralWidget)
        self.app_list_widget.setObjectName("app_list_widget")
        self.app_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.app_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.app_list_widget.setFocusPolicy(Qt.NoFocus)
        self.app_list_widget.setFlow(QListWidget.LeftToRight)
        self.app_list_widget.setIconSize(QSize(icon_width, icon_width))
        self.app_list_widget.setFrameShape(QListWidget.NoFrame)

        self.app_list_widget.doubleClicked.connect(lambda: self.double_clicked())

        for index in self.app_info_dict:
            app_info = self.app_info_dict[index]
            item = FatherQListWidgetItem()
            item.setSizeHint(QSize(icon_width, icon_height))
            if self.app_setting.use_rgb:
                item.setIcon(QIcon(app_info.icon_path))
            else:
                item.setIcon(QIcon(app_info.icon_gray_path))
            item.setWhatsThis(app_info.name)
            self.app_list_widget.addItem(item)

        self.setting = Setting(self.app_setting)
        self.setting.before_close_signal.connect(self.echo)

        self.message_label = QLabel("QQ：\n小冰：晚饭吃什么啊？",self.centralWidget)
        self.message_label.setGeometry(QRect(5, 2, message_window_width, message_window_height))
        self.message_label.setObjectName("message_label")

        self.drag_label = FatherQLabel("Input", self, self.centralWidget)
        self.drag_label.setGeometry(QRect(5 + message_window_width + 5, 2, input_window_width, input_window_height))
        self.drag_label.setObjectName("drag_label")

        # 显示选择目标设备按钮
        self.device_list_widget = QListWidget(self.centralWidget)
        self.device_list_widget.setGeometry(0, 0, 0, 0)
        self.device_list_widget.setFlow(QListWidget.LeftToRight)
        self.device_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.device_list_widget.setFrameShape(QListWidget.NoFrame)
        self.device_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.device_list_widget.clicked.connect(lambda: self.device_clicked_list_widget_fun())

        if len(self.app_info_dict) == 0:
            self.main_window.resize(
                5 + message_window_width + 5 + input_window_width + 5 + icon_width + 5,
                window_height)
            self.app_list_widget.setGeometry(
                QRect(5 + message_window_width + 5 + input_window_width + 5, 2, icon_width,
                      icon_height))
        else:
            self.main_window.resize(
                5 + message_window_width + 5 + input_window_width + 5 + icon_width * len(self.app_info_dict) + 5,
                window_height)
            self.app_list_widget.setGeometry(
            QRect(5 + message_window_width + 5 + input_window_width + 5, 2, icon_width * len(self.app_info_dict), icon_height))
        # self.main_layout.removeWidget(self.app_list_widget)

        """
            测试布局时使用：
            QListView#app_list_widget{
                color:black;
                background-color:rgb(255, 255, 0);
            }
            QLabel#message_label{
                color:black;
                background-color:rgb(255, 0, 255);
            }
            FatherQLabel#drag_label{
                color:black;
                background-color:rgb(0, 255, 255);
            }
        """

        self.main_window.setStyleSheet('''
            QListView::item:selected{
                color:black;
                background-color:rgba(255, 0, 0, 0);
            }
            QWidget#centralWidget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-left:1px solid darkGray;
                border-top-right-radius:10px;
                border-top-left-radius:10px;
                border-bottom-right-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

    def echo(self, int_value):
        # self.setWindowFlags()
        print(int_value)

    def double_clicked(self):
        name = self.app_list_widget.currentItem().whatsThis()
        app_info = self.app_info_dict[name]
        print(app_info.name, app_info.path)

        self.app_list_widget.currentItem().setIcon(QIcon(app_info.icon_path))
        handle = win32process.CreateProcess(app_info.path, '', None, None, 0, win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO())
        self.app_run_info_dict[name] = handle

    def set_self_message(self, message):
        print("{}{}".format(TAG, message))
        message =  message.split("+0~^D")
        order = message[0]
        data = message[1]
        if order == '1':
            data = data.split(":")
            for one_device in data:
                print(one_device)
            #     self.message_label.setText(one_device)
            #     self.socket_thread.send_file(one_device)

            self.message_label.setGeometry(0, 0, 0, 0)
            self.device_list_widget.setGeometry(5, 2, device_select_width, device_select_height)

            for one_device in data:
                print(one_device)
                item = QListWidgetItem()
                item.setSizeHint(QSize(device_select_item_width, device_select_item_height))
                item.setText(one_device)
                item.setWhatsThis(one_device)
                self.device_list_widget.addItem(item)
        elif order == '4':
            self.message_label.setText(data)

    def device_clicked_list_widget_fun(self):
        print("device_select_clicked")
        select_device = self.device_list_widget.currentItem().whatsThis()
        print('device_list_widget 已选择：{}'.format(select_device))
        self.socket_thread.send_file(select_device)
        self.device_list_widget.setGeometry(0, 0, 0, 0)
        self.device_list_widget.clear()
        self.message_label.setGeometry(QRect(5, 2, message_window_width, message_window_height))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = FatherQMainWindow()
    dock_main_ui = DockMain()
    dock_main_ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    # pyinstaller -F -w -i images/easydock.ico dock_main.py
    # 或
    # pyinstaller -F -c -i images/easydock.ico dock_main.py
    # (建议先用 - c，这样如果打包不成功的话可以看到哪里有错）