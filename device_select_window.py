import sys

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QSize, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QListWidget, QListWidgetItem, \
    QApplication

import json

from default_config import *


class DeviceSelectWindow(QFrame):
    '''自定义窗口'''
    # 知识点：
    # 1.为了得到返回值用到了自定义的信号/槽
    # 2.为了显示动态数字，使用了计时器

    before_close_signal = pyqtSignal(str, str)  # 自定义信号（int类型）

    def __init__(self):
        super().__init__()

        self.sec = 0
        self.setWindowTitle('自定义窗口')
        self.move(0,0)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.Tool)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # dialog.setWindowFlags(QtCore.Qt.Widget)  # 取消置顶
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        # self.send_message_btn = QPushButton(self, text="发送")
        # self.send_message_btn.setObjectName('send_message_btn')

        self.close_btn = QPushButton(self)
        self.close_btn.setText("×")

        self.close_btn.setObjectName("close_btn")

        #
        # self.layout_message_tip = QVBoxLayout(self)
        # self.layout_message_tip.setObjectName("layout_message_tip")
        # self.layout_message_tip.addWidget(self.send_message_btn)
        self.close_btn.setGeometry(5, 20, 20, 20)
        # 30
        # 50

        # self.setLayout(self.layout_message_tip)

        # 显示选择目标设备按钮
        self.device_list_widget = QListWidget(self)

        self.device_list_widget.setFlow(QListWidget.LeftToRight)
        self.device_list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.device_list_widget.setFrameShape(QListWidget.NoFrame)
        self.device_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.device_list_widget.clicked.connect(lambda: self.device_clicked_list_widget_fun())


        # self.setStyleSheet('''
        #     .QWidget{
        #         border:2px solid darkGray;
        #         border-top-right-radius:15px;
        #         border-top-left-radius:15px;
        #         border-bottom-right-radius:15px;
        #         border-bottom-left-radius:15px;
        #         background:white;
        #     }''')
        self.send_type = ''
        self.timer = QTimer()

        # self.send_message_btn.clicked.connect(self.send_message_function)
        self.close_btn.clicked.connect(self.close_self)

        self.timer.timeout.connect(self.update)  # 每次计时结束，触发update

    def start(self, device_list, send_type):
        self.send_type = send_type
        self.sec = 1
        self.timer.start(1000)
        print(len(device_list))

        for one_device in device_list:
            print(one_device)
            one_device = json.loads(one_device)
            item = QListWidgetItem(self.device_list_widget)
            item.setSizeHint(QSize(device_select_item_width, device_select_item_height))
            item.setText(one_device['name'][0:3] + '.')
            item.setWhatsThis(one_device['name'])
            self.device_list_widget.addItem(item)
        #

        self.device_list_widget.setGeometry(30, 10, len(device_list) * device_select_item_width, device_select_height)
        # self.send_message_btn.setGeometry(30 + len(device_list) * device_select_item_width, 10, 40, 40)
        self.resize(50 + len(device_list) * device_select_item_width, 60)

        self.setStyleSheet('''
                    QPushButton#close_btn{
                        background:red;
                        border:1px solid darkGray;
                        border-top-right-radius:10px;
                        border-top-left-radius:10px;
                        border-bottom-right-radius:10px;
                        border-bottom-left-radius:10px;
                        color:white;
                    }
                    QPushButton#close_btn:hover{
                        color:red;
                        background:white;
                    }
                    QListWidget{
                        text-transform: uppercase;
                        text-align: center;
                    }
                    QListWidget::Item{
                        border:2px solid white;
                        border-top-right-radius:20px;
                        border-top-left-radius:20px;
                        border-bottom-right-radius:20px;
                        border-bottom-left-radius:20px;
                        background:yellow;
                        margin-left: 5px;
                        margin-right: 5px;
                    }
                    QListWidget::Item:hover{
                        background:skyblue;
                        color:white;
                    }
                    DeviceSelectWindow{
                        border:2px solid darkGray;
                        border-top-right-radius:15px;
                        border-top-left-radius:15px;
                        border-bottom-right-radius:15px;
                        border-bottom-left-radius:15px;
                        background:white;
                    }
                ''')
        desktop = QApplication.desktop()
        self.move(desktop.width() * 0.6, desktop.height() * 0.4)
        """
        QSS：：
setStyleSheet('QListWidget{border:1px solid gray; color:black; }'
'QListWidget::Item{padding-top:-2px; padding-bottom:-1px;}'
"QListWidget::Item:hover{background:skyblue;padding-top:0px; padding-bottom:0px; }"
"QListWidget::item:selected{background:lightgray; color:red; }"
"QListWidget::item:selected:!active{active{border-width:0px;background:lightgreen; }")
                    QPushButton#send_message_btn{
                        background:red;
                        border:1px solid darkGray;
                        border-top-right-radius:20px;
                        border-top-left-radius:20px;
                        border-bottom-right-radius:20px;
                        border-bottom-left-radius:20px;
                        color:white;
                    }
                    QPushButton#send_message_btn:hover{
                        color:red;
                        background:white;
                    }
"""

    def update(self):
        self.sec += 1
        if self.sec == 6:
            self.timer.stop()
            self.before_close_signal.emit('-1', '-1')  # 发送信号，带参数 0
            self.hide()

    def close_self(self):
        self.timer.stop()
        self.before_close_signal.emit('-1', '-1')  # 发送信号，带参数 0
        self.hide()


    # def send_message_function(self):
    #     self.timer.stop()
    #     self.before_close_signal.emit(1)  # 发送信号，带参数 1
    #     self.sec = 0
    #     self.hide()

    # # 默认关闭事件
    # def closeEvent(self, e):
    #     self.timer.stop()
    #     self.before_close_signal.emit(0)  # 发送信号，带参数 0
    #     self.sec = 0
    #     self.hide()

    def device_clicked_list_widget_fun(self):
        self.hide()
        self.timer.stop()
        select_device = self.device_list_widget.currentItem().whatsThis()
        print('device_list_widget 已选择：{}'.format(select_device))

        self.device_list_widget.clear()
        self.before_close_signal.emit(select_device, self.send_type)  # 发送信号，带参数 1
