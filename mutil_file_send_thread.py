#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-21 下午8:32
# @Author  : Yaque
# @File    : server_socket_文件客户端.py
# @Software: PyCharm

from PyQt5.QtCore import QThread, pyqtSignal, QMutex

import socket
from socket import *
import json
import struct
import time
import os
import traceback

from tools.net_tools import unpackage_data_2_security, package_data_2_security ,data2byte, byte2data
from tools.file_tools import get_file_inform, split_file, composite_file
from tools.md5 import getmd5

TAG = "tools_sockt_client:     "
buffsize = 1024


qmut_tool = QMutex() # 创建线程锁


class FileSendQThread(QThread):
    my_signal = pyqtSignal(str)
    is_connection = False

    def __init__(self, file_path, ip, port, aim_device):
        super(FileSendQThread, self).__init__()
        self.ip = ip
        self.port = port
        self.aim_device = aim_device
        self.file_path = file_path

    def run(self):
        print(self.ip, self.port)
        self.tcp_client = socket(AF_INET, SOCK_STREAM)
        ip_port = ((self.ip, int(self.port)))
        self.tcp_client.connect_ex(ip_port)
        print("开始第一次发送文件")
        out_flag = False
        while not out_flag:
            try:
                self.send_file()
                confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
                if confirm_data == 911000:
                    print("NetThreadSendFileLite文件拆分包发送完成")
                    os.remove(self.file_path)
                    out_flag = True
                elif confirm_data == 911002:
                    print("NetThreadSendFileLite文件拆分包发送出现错误")
                else:
                    print("未知错误")
                    out_flag = True
            except:
                print(traceback.format_exc())

        self.tcp_client.close()


    def send_file(self):
        head_info_len, head_info, file_size = get_file_inform(self.file_path, self.aim_device)
        print(head_info)
        self.tcp_client.send(package_data_2_security(data2byte(11000)))
        confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
        if confirm_data == 911000:
            head_info_buffer = head_info.encode('utf-8')
            head_info_buffer = package_data_2_security(head_info_buffer)
            head_info_len_buffer = data2byte(len(head_info_buffer))
            head_info_len_buffer = package_data_2_security(head_info_len_buffer)
            self.tcp_client.send(head_info_len_buffer)  # 这里是4个字节
            self.tcp_client.send(head_info_buffer)  # 发送报头的内容

            s = time.time()
            counter = 0
            with open(self.file_path, 'rb') as sf:
                while True:
                    data = sf.read(1024)
                    data_len = len(data)
                    if data_len == 0:
                        break
                    elif data_len == 1024:
                        data = data + data2byte(counter)
                    elif data_len < 1024:
                        for i in range(data_len, 1024):
                            data += b'0'
                        data = data + data2byte(counter)
                    timeout_counter = 0
                    while True:
                        try:
                            self.tcp_client.send(package_data_2_security(data))
                            confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
                            if confirm_data == 911000:
                                # print(data)
                                # print(len(data))
                                # print(counter)
                                counter += 1
                                timeout_counter = 0
                                break
                        except socket.timeout as e:
                            timeout_counter += 1
                            print(e.args)
                            print(traceback.format_exc())
                            print("大文件数据发送超时，尝试重新发送")
                            if timeout_counter == 5:
                                return