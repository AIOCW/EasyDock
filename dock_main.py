import os
import sys
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from windows_api import get_handle
import sys
import traceback
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget

from setting import Setting

from father_q_main_window import FatherQMainWindow
from father_q_list_widget import FatherQListWidget
from father_q_label import FatherQLabel
from father_q_list_widget_item import FatherQListWidgetItem

from dao.app_info_dao import select

from data_manager.app_setting_location import select_setting

from default_config import *

from tools_socket_client import SocketQThread

from tools.net_tools import str_2_json

from message_tip_window import MessageTipWindow
from device_select_window import DeviceSelectWindow
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

        self.init_some_function()

        self.init_ui()

    def init_config(self):
        # init_table_data_for_setting()
        self.app_setting = select_setting()


    def init_thead(self):
        try:
            self.socket_thread = SocketQThread(self.app_setting)
            self.socket_thread.my_signal.connect(self.set_self_message)
            self.socket_thread.start()
        except:
            print(traceback.format_exc())

    def init_data(self):
        self.need_show_send = True

        for app_info in select():
            self.app_info_dict[app_info.name] = app_info

    def init_some_function(self):
        self.clipboard = QApplication.clipboard()  # 1
        self.clipboard.dataChanged.connect(lambda: self.clipboard_data_changed())
        self.message_tip_window = MessageTipWindow()  # 自定义窗口
        self.message_tip_window.before_close_signal.connect(self.show_message)
        self.device_select_window = DeviceSelectWindow()
        self.device_select_window.before_close_signal.connect(self.send_message)
        # self.clipboard.dataChanged.connect(lambda: print('Data Changed'))


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
        handle = get_handle(app_info)
        self.app_run_info_dict[name] = handle

    def set_self_message(self, message):
        print("{}{}".format(TAG, message))
        message = message.split("+0~^D")
        order = message[0]
        data = message[1]
        if order == 'f1001':
            json_data_list = str_2_json(data)
            self.device_select_window.show()
            self.device_select_window.start(json_data_list, order)
        elif order == 't1001':
            json_data_list = str_2_json(data)
            self.device_select_window.show()
            self.device_select_window.start(json_data_list, "t")
        elif order == '91011':
            self.need_show_send = False
            self.clipboard.setText(data)
            # pyperclip.paste()
            self.message_tip_window.show()
            self.message_tip_window.start(data)
        elif order == '91100':
            # pyperclip.paste()
            self.message_tip_window.show()
            self.message_tip_window.start(data)
        elif order == '4':
            self.message_label.setText(data)

    def clipboard_data_changed(self):
        print("clipboard data change")
        # self.clipboard.setText()
        if self.need_show_send:
            self.socket_thread.get_other_client_data_api("", "t")
        else:
            self.need_show_send = True


    def send_message(self, value, send_type):
        print(value)
        if value != '-1':
            if send_type == 't':
                text_message = self.clipboard.text()
                if text_message != '':
                    self.socket_thread.send_text_message_api(text_message, value)
            elif send_type == 'f1001':
                self.socket_thread.send_file_api(value)
        else:
            return

    def show_message(self, value):
        print(value)

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