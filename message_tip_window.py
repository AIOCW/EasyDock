from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QApplication


class MessageTipWindow(QFrame):
    '''自定义窗口'''
    # 知识点：
    # 1.为了得到返回值用到了自定义的信号/槽
    # 2.为了显示动态数字，使用了计时器

    before_close_signal = pyqtSignal(int)  # 自定义信号（int类型）

    def __init__(self):
        super().__init__()

        self.sec = 0
        self.setWindowTitle('自定义窗口')
        self.resize(200, 60)
        self.move(0,0)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.Tool)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # dialog.setWindowFlags(QtCore.Qt.Widget)  # 取消置顶
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        self.read_message_btn = QPushButton(self, text="发送")
        self.read_message_btn.setObjectName('read_message_btn')

        self.close_btn = QPushButton(self)

        self.close_btn.setText("×")
        self.close_btn.setObjectName("close_btn")

        self.show_text_message_label = QLabel(self)


        #
        # self.layout_message_tip = QVBoxLayout(self)
        # self.layout_message_tip.setObjectName("layout_message_tip")
        # self.layout_message_tip.addWidget(self.send_message_btn)
        self.close_btn.setGeometry(5, 20, 20, 20)

        # self.setLayout(self.layout_message_tip)

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
                    QPushButton#read_message_btn{
                        background:red;
                        border:1px solid darkGray;
                        border-top-right-radius:20px;
                        border-top-left-radius:20px;
                        border-bottom-right-radius:20px;
                        border-bottom-left-radius:20px;
                        color:white;
                    }
                    QPushButton#read_message_btn:hover{
                        color:red;
                        background:white;
                    }
                    MessageTipWindow{
                        border:2px solid darkGray;
                        border-top-right-radius:15px;
                        border-top-left-radius:15px;
                        border-bottom-right-radius:15px;
                        border-bottom-left-radius:15px;
                        background:white;
                    }
        ''')

        self.timer = QTimer()

        self.read_message_btn.clicked.connect(self.read_message_function)
        self.close_btn.clicked.connect(self.close_self)

        self.timer.timeout.connect(self.update)  # 每次计时结束，触发update

    def start(self, text_message):
        self.sec = 0
        self.timer.start(1000)
        text_size = 11
        self.show_text_message_label.setGeometry(30, 10, len(text_message) * text_size, 40)
        self.read_message_btn.setGeometry(30 + len(text_message) * text_size + 10, 10, 40, 40)
        self.resize(30 + len(text_message) * text_size + 10 + 45, 60)
        self.show_text_message_label.setText(text_message)
        desktop = QApplication.desktop()
        self.move(desktop.width() * 0.6, desktop.height() * 0.4)


    def update(self):
        self.sec += 1
        if self.sec == 6:
            self.timer.stop()
            self.before_close_signal.emit(0)  # 发送信号，带参数 0
            self.hide()

    def close_self(self):
        self.timer.stop()
        self.before_close_signal.emit(0)  # 发送信号，带参数 0
        self.sec = 0
        self.hide()

    def read_message_function(self):
        self.timer.stop()
        self.before_close_signal.emit(1)  # 发送信号，带参数 1
        self.sec = 0
        self.hide()

    # # 默认关闭事件
    # def closeEvent(self, e):
    #     self.timer.stop()
    #     self.before_close_signal.emit(0)  # 发送信号，带参数 0
    #     self.sec = 0
    #     self.hide()
