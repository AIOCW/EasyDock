import sys
from PyQt5.Qt import QIcon, QCursor
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QCheckBox

from data_manager.app_setting_location import update_setting

title_data = ["网络设置", "文件传输设置", "粘贴管理", "系统状态", "消息管理"]


class Setting(QWidget):
    before_close_signal = pyqtSignal(int)

    def __init__(self, app_setting):
        super(Setting, self).__init__()

        self.app_setting = app_setting

        # self.setWindowOpacity(0.8)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        self.setWindowIcon(QIcon("images/easydock.ico"))
        self.setWindowTitle("Ass设置")
        self.init_base_ui()
        self.init_click_listen()


    def init_base_ui(self):
        self.h_layout = QHBoxLayout()
        self.setFixedWidth(500)
        self.setFixedHeight(300)

        self.close_button = QPushButton("关闭")
        self.close_button.setFixedHeight(280)
        self.close_button.setFixedWidth(50)

        self.setting_title_list = QListWidget(self)
        self.setting_title_list.setFixedWidth(130)
        self.setting_detailed_list = QListWidget(self)

        for i, title in enumerate(title_data):
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setWhatsThis(str(i))
            item.setSizeHint(QSize(50, 50))  # 设置QListWidgetItem大小
            widget = self.get_item_widget(title)  # 调用上面的函数获取对应
            self.setting_title_list.addItem(item)  # 添加item
            self.setting_title_list.setItemWidget(item, widget)  # 为item设置widget

        self.get_items_net()
        self.get_items_file()
        self.get_items_paste()

        self.h_layout.addWidget(self.setting_title_list)
        self.h_layout.addWidget(self.setting_detailed_list)
        self.h_layout.addWidget(self.close_button)

        self.setStyleSheet('''
            QListWidgetItem#item{
                background:white;
            }
            QListWidget#setting_title_list{
                color:black;
                background-color:rgba(255, 0, 0, 0);
            }
            Setting{
                color:#232C51;  
                border-top:2px solid darkGray;
                border-bottom:2px solid darkGray;
                border-right:2px solid darkGray;
                border-left:2px solid darkGray;
                border-top-right-radius:10px;
                border-top-left-radius:10px;
                border-bottom-right-radius:10px;
                border-bottom-left-radius:10px;
                
            }
        ''')

        self.setLayout(self.h_layout)

    def init_click_listen(self):
        self.setting_title_list.clicked.connect(lambda: self.title_click())

        self.close_button.clicked.connect(lambda: self.close_button_fun())

    def title_click(self):
        print("title_clicked")
        item = QListWidgetItem(self.setting_title_list.currentItem())
        print(item.whatsThis())
        if item.whatsThis() == '0':
            self.setting_detailed_list.setCurrentRow(0)
        elif item.whatsThis() == '1':
            self.setting_detailed_list.setCurrentRow(4)
        elif item.whatsThis() == '2':
            self.setting_detailed_list.setCurrentRow(6)
        elif item.whatsThis() == '3':
            print("现在没有写")
            pass
        elif item.whatsThis() == '4':
            print("现在没有写")
            pass

    def close_button_fun(self):
        print("关闭设置界面")
        self.before_close_signal.emit(88)  # 发送信号，带参数 888
        self.close()  # 然后窗口关闭

    def get_item_widget(self, title):

        wight = QWidget()

        # 总体横向布局
        layout_main = QHBoxLayout()
        title = QLabel(title)
        layout_main.addWidget(title)
        wight.setLayout(layout_main)  # 布局给wight
        return wight  # 返回wight

    def get_items_net(self):
        # 服务器IP设置选项
        widget_ip = QWidget()
        layout_ip = QVBoxLayout()
        layout_h_ip = QHBoxLayout()

        ip_title = QLabel("服务器IP地址")
        ip_edit = QLineEdit()
        ip_edit.setText(self.app_setting.ip)
        ip_button = QPushButton("应用")

        layout_h_ip.addWidget(ip_edit)
        layout_h_ip.addWidget(ip_button)

        layout_ip.addWidget(ip_title)
        layout_ip.addLayout(layout_h_ip)

        widget_ip.setLayout(layout_ip)  # 布局给wight

        net_item_ip = QListWidgetItem()
        net_item_ip.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(net_item_ip)
        self.setting_detailed_list.setItemWidget(net_item_ip, widget_ip)

        ip_button.clicked.connect(lambda: self.ip_button_fun(ip_edit))

        # 远程服务器IP设置选项
        widget_remove_ip = QWidget()
        layout_remove_ip = QVBoxLayout()
        layout_h_remove_ip = QHBoxLayout()

        remove_ip_title = QLabel("远程服务器IP地址")
        remove_ip_edit = QLineEdit()
        remove_ip_edit.setText(self.app_setting.remove_ip)
        remove_ip_button = QPushButton("应用")

        layout_h_remove_ip.addWidget(remove_ip_edit)
        layout_h_remove_ip.addWidget(remove_ip_button)

        layout_remove_ip.addWidget(remove_ip_title)
        layout_remove_ip.addLayout(layout_h_remove_ip)

        widget_remove_ip.setLayout(layout_remove_ip)  # 布局给wight

        net_item_remove_ip = QListWidgetItem()
        net_item_remove_ip.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(net_item_remove_ip)
        self.setting_detailed_list.setItemWidget(net_item_remove_ip, widget_remove_ip)

        remove_ip_button.clicked.connect(lambda: self.remove_ip_button_fun(remove_ip_edit))

        # 服务器端口设置选项
        widget_port = QWidget()
        layout_port = QVBoxLayout()
        layout_h_prot = QHBoxLayout()
        port_title = QLabel("服务器端口号")
        port_edit = QLineEdit()
        port_edit.setText(self.app_setting.port)
        port_button = QPushButton("应用")

        layout_h_prot.addWidget(port_edit)
        layout_h_prot.addWidget(port_button)

        layout_port.addWidget(port_title)
        layout_port.addLayout(layout_h_prot)
        widget_port.setLayout(layout_port)

        net_item_port = QListWidgetItem()
        net_item_port.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(net_item_port)
        self.setting_detailed_list.setItemWidget(net_item_port, widget_port)

        port_button.clicked.connect(lambda: self.port_button_fun(port_edit))

        # 助手代号设置选项
        widget_ass_number = QWidget()
        layout_ass_number = QVBoxLayout()
        layout_h_ass_number = QHBoxLayout()

        ass_number_title = QLabel("助手代号")
        ass_number_edit = QLineEdit()
        ass_number_edit.setText(self.app_setting.device_name)
        ass_number_button = QPushButton("应用")

        layout_h_ass_number.addWidget(ass_number_edit)
        layout_h_ass_number.addWidget(ass_number_button)

        layout_ass_number.addWidget(ass_number_title)
        layout_ass_number.addLayout(layout_h_ass_number)

        widget_ass_number.setLayout(layout_ass_number)

        net_item_ass_number = QListWidgetItem()
        net_item_ass_number.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(net_item_ass_number)
        self.setting_detailed_list.setItemWidget(net_item_ass_number, widget_ass_number)

        ass_number_button.clicked.connect(lambda :self.ass_number_button_fun(ass_number_edit))

    def ip_button_fun(self, ip_edit):
        server_address = ip_edit.text()
        print(server_address)
        update_setting(server_address, 'ip')

    def remove_ip_button_fun(self, remove_ip_edit):
        server_address = remove_ip_edit.text()
        print(server_address)
        update_setting(server_address, 'remove_ip')

    def port_button_fun(self, port_edit):
        server_port = port_edit.text()
        print(server_port)
        update_setting(server_port, 'port')

    def ass_number_button_fun(self, ass_number_edit):
        ass_number = ass_number_edit.text()
        print(ass_number)
        update_setting(ass_number, 'device_name')

    def get_items_file(self):
        widget_address = QWidget()
        # 总体横向布局
        layout_address = QVBoxLayout()
        layout_h_address = QHBoxLayout()
        file_address_title = QLabel("本机文件保存地址")
        file_address_edit = QLineEdit()
        file_address_edit.setText(self.app_setting.file_local_save_name)
        file_address_button = QPushButton("应用")

        layout_h_address.addWidget(file_address_edit)
        layout_h_address.addWidget(file_address_button)


        layout_address.addWidget(file_address_title)
        layout_address.addLayout(layout_h_address)
        widget_address.setLayout(layout_address)  # 布局给wight

        file_item_address = QListWidgetItem()
        file_item_address.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(file_item_address)
        self.setting_detailed_list.setItemWidget(file_item_address, widget_address)

        file_address_button.clicked.connect(lambda :self.file_address_button_fun(file_address_edit))


        # 是否显示图片
        widget_show_image = QWidget()
        # 总体横向布局
        layout_show_image = QVBoxLayout()
        layout_h_show_image = QHBoxLayout()
        open_image_title = QLabel("图片是否自动打开")
        open_image_check_box = QCheckBox()
        if self.app_setting.auto_open_image == 1:
            open_image_check_box.setCheckState(Qt.Checked) # 2
        else:
            open_image_check_box.setCheckState(Qt.Unchecked)
        layout_show_image.addWidget(open_image_title)
        layout_show_image.addWidget(open_image_check_box)
        widget_show_image.setLayout(layout_show_image)  # 布局给wight

        file_item_show_image = QListWidgetItem()
        file_item_show_image.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(file_item_show_image)
        self.setting_detailed_list.setItemWidget(file_item_show_image, widget_show_image)

        open_image_check_box.stateChanged.connect(lambda: self.open_image_check_box_fun(open_image_check_box))  # 3

    def file_address_button_fun(self, file_address_edit):
        file_address = file_address_edit.text()
        print(file_address)
        update_setting(file_address, 'file_local_save_name')

    def open_image_check_box_fun(self, open_image_check_box):
        print('{} was clicked, and its current state is {}'.format(open_image_check_box.text(), open_image_check_box.checkState()))
        if open_image_check_box.checkState() == Qt.Checked:
            update_setting(1, 'auto_open_image')
        else:
            update_setting(0, 'auto_open_image')

    def get_items_paste(self):
        # 是否显示图片
        widget_aotu_paste = QWidget()
        # 总体横向布局
        layout_aotu_paste = QVBoxLayout()
        layout_h_auto_paste = QHBoxLayout()

        open_paste_title = QLabel("检测自动粘贴是否打开")
        open_paste_check_box = QCheckBox()
        if self.app_setting.auto_check_paste == 1:
            open_paste_check_box.setCheckState(Qt.Checked)
        else:
            open_paste_check_box.setCheckState(Qt.Unchecked)

        layout_aotu_paste.addWidget(open_paste_title)
        layout_aotu_paste.addWidget(open_paste_check_box)
        widget_aotu_paste.setLayout(layout_aotu_paste)  # 布局给wight

        paste_item_auto_paste = QListWidgetItem()
        paste_item_auto_paste.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(paste_item_auto_paste)
        self.setting_detailed_list.setItemWidget(paste_item_auto_paste, widget_aotu_paste)
        open_paste_check_box.stateChanged.connect(lambda: self.open_paste_check_box_fun(open_paste_check_box))

        # 是否显示彩色图标
        widget_use_rgb = QWidget()
        # 总体横向布局
        layout_use_rgb = QVBoxLayout()
        layout_h_use_rgb = QHBoxLayout()

        use_rgb_title = QLabel("是否显示彩色图标")
        use_rgb_check_box = QCheckBox()
        if self.app_setting.use_rgb == 1:
            use_rgb_check_box.setCheckState(Qt.Checked)
        else:
            use_rgb_check_box.setCheckState(Qt.Unchecked)

        layout_use_rgb.addWidget(use_rgb_title)
        layout_use_rgb.addWidget(use_rgb_check_box)
        widget_use_rgb.setLayout(layout_use_rgb)  # 布局给wight

        icon_item_use_rgb = QListWidgetItem()
        icon_item_use_rgb.setSizeHint(QSize(200, 70))
        self.setting_detailed_list.addItem(icon_item_use_rgb)
        self.setting_detailed_list.setItemWidget(icon_item_use_rgb, widget_use_rgb)
        use_rgb_check_box.stateChanged.connect(lambda: self.use_rgb_check_box_fun(use_rgb_check_box))

    def open_paste_check_box_fun(self, open_paste_check_box):
        print("{}被操作，其操作状态时{}".format(open_paste_check_box.text(), open_paste_check_box.checkState()))
        if open_paste_check_box.checkState() == Qt.Checked:
            update_setting(1, 'auto_check_paste')
        else:
            update_setting(0, 'auto_check_paste')

    def use_rgb_check_box_fun(self, use_rgb_check_box):
        print("{}被操作，其操作状态时{}".format(use_rgb_check_box.text(), use_rgb_check_box.checkState()))
        if use_rgb_check_box.checkState() == Qt.Checked:
            update_setting(1, 'use_rgb')
        else:
            update_setting(0, 'use_rgb')

    # drag window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Setting()
    demo.show()
    sys.exit(app.exec_())