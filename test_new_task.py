from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5 import QtCore
from PyQt5.Qt import QIcon
import sys

from setting import Setting
from test_by_self import MyWindow2

class MyWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.resize(400, 300)
        self.setWindowTitle("Ass")
        self.setWindowIcon(QIcon("images/icon.png"))
        # https://www.easyicon.net/1188455-Fingerprint_icon.html
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        # dialog.setWindowFlags(QtCore.Qt.Widget)  # 取消置顶
        # self.setWindowOpacity(0.8)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        # 全局布局（注意参数 self）
        wl = QVBoxLayout(self)

        # 局部布局
        h1 = QHBoxLayout()  # 输入框
        h2 = QHBoxLayout()  # 消息窗口
        h3 = QHBoxLayout()  # 文件（夹）打开，保存
        h4 = QHBoxLayout()  # 颜色、字体、自定义

        btn11 = QPushButton('输入：整数')
        btn12 = QPushButton('输入：小数')
        btn13 = QPushButton('输入：文本')
        btn14 = QPushButton('输入：多文')
        btn15 = QPushButton('输入：选项')

        btn21 = QPushButton('消息：信息')
        btn22 = QPushButton('消息：问答')
        btn23 = QPushButton('消息：警告')
        btn24 = QPushButton('消息：危险')
        btn25 = QPushButton('消息：关于')

        btn31 = QPushButton('文件：文件夹')
        btn32 = QPushButton('文件：单文件')
        btn33 = QPushButton('文件：多文件')
        btn34 = QPushButton('文件：保存')
        btn35 = QPushButton('文件：另存为')

        btn41 = QPushButton('颜色')
        btn42 = QPushButton('字体')
        btn43 = QPushButton('自定义')

        for btn in (btn11, btn12, btn13, btn14, btn15):
            h1.addWidget(btn)

        for btn in (btn21, btn22, btn23, btn24, btn25):
            h2.addWidget(btn)

        for btn in (btn31, btn32, btn33, btn34, btn35):
            h3.addWidget(btn)

        for btn in (btn41, btn42, btn43):
            h4.addWidget(btn)

        btn11.clicked.connect(self.do_btn11)  # 输入：整数
        btn12.clicked.connect(self.do_btn12)  # 输入：小数
        btn13.clicked.connect(self.do_btn13)  # 输入：文本
        btn14.clicked.connect(self.do_btn14)  # 输入：多文
        btn15.clicked.connect(self.do_btn15)  # 输入：选项

        btn21.clicked.connect(self.do_btn21)  # 消息：信息
        btn22.clicked.connect(self.do_btn22)  # 消息：问答
        btn23.clicked.connect(self.do_btn23)  # 消息：警告
        btn24.clicked.connect(self.do_btn24)  # 消息：危险
        btn25.clicked.connect(self.do_btn25)  # 消息：关于

        btn31.clicked.connect(self.do_btn31)  # 文件：文件夹
        btn32.clicked.connect(self.do_btn32)  # 文件：单文件
        btn33.clicked.connect(self.do_btn33)  # 文件：多文件
        btn34.clicked.connect(self.do_btn34)  # 文件：保存
        btn35.clicked.connect(self.do_btn35)  # 文件：另存为

        btn41.clicked.connect(self.do_btn41)  # 颜色
        btn42.clicked.connect(self.do_btn42)  # 字体
        btn43.clicked.connect(self.do_btn43)  # 自定义

        # 加到全局布局
        wl.addLayout(h1)
        wl.addLayout(h2)
        wl.addLayout(h3)
        wl.addLayout(h4)

        self.window2 = Setting()  # 自定义窗口
        self.window2.before_close_signal.connect(self.echo)  # 接收自定义窗口关闭时发送过来的信号，交给 echo 函数显示

    def echo(self, value):
        '''显示对话框返回值'''
        # QMessageBox.information(self, "返回值", "得到：{}\n\ntype: {}".format(value, type(value)),
                                # QMessageBox.Yes | QMessageBox.No)
        print(value)
        # pass

    # =====================================================================
    def do_btn11(self, event):  # 输入：整数
        # 后面四个数字的作用依次是 初始值 最小值 最大值 步幅
        value, ok = QInputDialog.getInt(self, "输入框标题", "这是提示信息\n\n请输入整数:", 37, -10000, 10000, 2)
        # self.echo(value)

    def do_btn12(self, event):  # 输入：小数
        # 后面四个数字的作用依次是 初始值 最小值 最大值 小数点后位数
        value, ok = QInputDialog.getDouble(self, "输入框标题", "这是提示信息\n\n请输入整数:", 37.56, -10000, 10000, 2)
        self.echo(value)

    def do_btn13(self, event):  # 输入：文本
        # 第三个参数表示显示类型，可选，有正常（QLineEdit.Normal）、密碼（ QLineEdit. Password）、不显示（ QLineEdit. NoEcho）三种情况
        value, ok = QInputDialog.getText(self, "输入框标题", "这是提示信息\n\n请输入文本:", QLineEdit.Normal, "这是默认值")
        self.echo(value)

    def do_btn14(self, event):  # 输入：多文
        value, ok = QInputDialog.getMultiLineText(self, "输入框标题", "这是提示信息\n\n请输入地址:", "默认的\n我的地址是\n中国广东广州番禺")
        self.echo(value)

    def do_btn15(self, event):  # 输入：选项
        # 1为默认选中选项目，True/False  列表框是否可编辑。
        items = ["Spring", "Summer", "Fall", "Winter"]
        value, ok = QInputDialog.getItem(self, "输入框标题", "这是提示信息\n\n请选择季节:", items, 1, True)
        self.echo(value)

    # =====================================================================
    def do_btn21(self, event):  # 消息：信息
        reply = QMessageBox.information(self,
                                        "消息框标题",
                                        "这是一条消息。",
                                        QMessageBox.Yes | QMessageBox.No)
        self.echo(reply)

    def do_btn22(self, event):  # 消息：问答
        reply = QMessageBox.question(self,
                                     "消息框标题",
                                     "这是一条问答吗？",
                                     QMessageBox.Yes | QMessageBox.No)
        self.echo(reply)

    def do_btn23(self, event):  # 消息：警告
        reply = QMessageBox.warning(self,
                                    "消息框标题",
                                    "这是一条警告！",
                                    QMessageBox.Yes | QMessageBox.No)
        self.echo(reply)

    def do_btn24(self, event):  # 消息：危险
        reply = QMessageBox.ctitical(self,
                                     "消息框标题",
                                     "危险！程序即将强制退出！！！\n\n这个按钮再也点不开。",
                                     QMessageBox.Yes | QMessageBox.No)
        self.echo(reply)

    def do_btn25(self, event):  # 消息：关于
        reply = QMessageBox.about(self,
                                  "消息框标题",
                                  "这是关于软件的说明。。。",
                                  QMessageBox.Yes | QMessageBox.No)
        self.echo(reply)

    # =====================================================================
    def do_btn31(self, event):  # 文件：文件夹
        dir = QFileDialog.getExistingDirectory(self,
                                               "选取文件夹",
                                               "C:/")  # 起始路径
        self.echo(dir)

    def do_btn32(self, event):  # 文件：单文件
        file_, filetype = QFileDialog.getOpenFileName(self,
                                                      "选取文件",
                                                      "C:/",
                                                      "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.echo(file_)

    def do_btn33(self, event):  # 文件：多文件
        files, ok = QFileDialog.getOpenFileNames(self,
                                                 "多文件选择",
                                                 "C:/",
                                                 "All Files (*);;Text Files (*.txt)")
        self.echo(files)

    def do_btn34(self, event):  # 文件：保存
        file_, ok = QFileDialog.getSaveFileName(self,
                                                "文件保存",
                                                "C:/",
                                                "All Files (*);;Text Files (*.txt)")
        self.echo(file_)

    def do_btn35(self, event):  # 文件：另存为
        file_, ok = QFileDialog.getSaveFileName(self,
                                                "文件另存为",
                                                "C:/",
                                                "All Files (*);;Text Files (*.txt)")
        self.echo(file_)

    # =====================================================================
    def do_btn41(self, event):  # 颜色
        color = QColorDialog.getColor(Qt.blue, self, "Select Color")
        self.echo(color)

    def do_btn42(self, event):  # 字体
        font, ok = QFontDialog.getFont()
        self.echo(font)

    def do_btn43(self, event):  # 自定义

        self.window2.show()




if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())