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


class FileRecvQThread(QThread):
    # my_signal = pyqtSignal(str)
    is_connection = False

    def __init__(self, number_name, ip, port):
        super(FileRecvQThread, self).__init__()
        self.ip = ip
        self.port = port
        self.number_name = number_name

    def run(self):
        print(self.ip, self.port)
        self.tcp_client = socket(AF_INET, SOCK_STREAM)
        ip_port = ((self.ip, int(self.port)))
        self.tcp_client.connect_ex(ip_port)
        print("开始一次接收文件")
        out_flag = False
        count_retry = 0
        while not out_flag:
            try:

                self.recv_file()
                confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
                count_retry = 0
                if confirm_data == 911000:
                    print("NetThreadSendFileLite文件拆分包发送完成")
                    os.remove(self.file_path)
                    out_flag = True
                elif confirm_data == 911002:
                    count_retry += 1
                    print("NetThreadSendFileLite文件拆分包发送出现错误")
                    if count_retry == 2:
                        break
                else:
                    print("未知错误")
                    out_flag = True
            except:
                count_retry += 1
                if count_retry == 2:
                    break
                print(traceback.format_exc())

        self.tcp_client.close()


    def recv_file(self):
        print("进入分片文件接收操作")
        confirm_code = package_data_2_security(data2byte(6633))
        self.tcp_client.send(confirm_code)

        flag_code = package_data_2_security(data2byte(int(self.number_name)))
        self.tcp_client.send(flag_code)

        print("开始接收分片文件信息")
        # 接受客户端介绍信息的长度
        json_data_len_buffer = self.tcp_client.recv(4)
        json_data_len_buffer_unpackage = unpackage_data_2_security(json_data_len_buffer)
        json_data_len = byte2data(json_data_len_buffer_unpackage)

        # 接受介绍信息的内容
        json_data_buffer = self.tcp_client.recv(json_data_len)
        json_data_buffer_unpackage = unpackage_data_2_security(json_data_buffer)
        print("数据接收完成")
        # 将介绍信息的内容反序列化
        json_data = json.loads(json_data_buffer_unpackage.decode('utf-8'))
        print("本次介绍信息的内容为：{}".format(json_data))
        print("本次file长度为：{}".format(json_data["filesize"]))

        recv_len = 0
        filename = json_data['filename']
        filesize = json_data['filesize']
        filepath = json_data['filepath']
        aim_device = json_data['aim_device']
        md5 = json_data['md5']
        with open("TempFile/" + filename, 'wb') as f:
            now_data_number = 0;
            c_retry = 0
            while recv_len < filesize:
                package_data_buffer = self.tcp_client.recv(1028)
                package_data_buffer_un = unpackage_data_2_security(package_data_buffer)
                # print("Data Length {}".format(len(package_data_buffer_un)))
                if len(package_data_buffer_un) == 1028:
                    file_buffer = package_data_buffer_un[0:1024]
                    data_number = byte2data(package_data_buffer_un[1024:1028])
                    # print("Now Data Number {}, Data Number {}, ".format(now_data_number, data_number))
                    if now_data_number == data_number:
                        if filesize - recv_len > buffsize:
                            recv_len += len(file_buffer)
                            f.write(file_buffer)
                        else:
                            end_size = filesize - recv_len
                            recv_len += end_size
                            f.write(file_buffer[0:end_size])
                        c_retry = 0
                        self.tcp_client.send(package_data_2_security(data2byte(941000)))
                        now_data_number += 1
                else:
                    self.tcp_client.send(package_data_2_security(data2byte(941001)))
                    c_retry += 1
                    if c_retry == 5:
                        print("error")
                        return
        new_file_md5 = getmd5("TempFile/" + filename)
        if new_file_md5 == md5:
            print("new_file_md5 {}, md5 {}".format(new_file_md5, md5))
            confirm_code = package_data_2_security(data2byte(941000))
            self.tcp_client.send(confirm_code)
        else:
            confirm_code = package_data_2_security(data2byte(941002))
            self.tcp_client.send(confirm_code)


        # head_info_len, head_info, file_size = get_file_inform(self.file_path, self.aim_device)
        # print(head_info)
        # self.tcp_client.send(package_data_2_security(data2byte(11000)))
        # confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
        # if confirm_data == 911000:
        #     head_info_buffer = head_info.encode('utf-8')
        #     head_info_buffer = package_data_2_security(head_info_buffer)
        #     head_info_len_buffer = data2byte(len(head_info_buffer))
        #     head_info_len_buffer = package_data_2_security(head_info_len_buffer)
        #     self.tcp_client.send(head_info_len_buffer)  # 这里是4个字节
        #     self.tcp_client.send(head_info_buffer)  # 发送报头的内容
        #
        #     s = time.time()
        #     counter = 0
        #     with open(self.file_path, 'rb') as sf:
        #         while True:
        #             data = sf.read(1024)
        #             data_len = len(data)
        #             if data_len == 0:
        #                 break
        #             elif data_len == 1024:
        #                 data = data + data2byte(counter)
        #             elif data_len < 1024:
        #                 for i in range(data_len, 1024):
        #                     data += b'0'
        #                 data = data + data2byte(counter)
        #             timeout_counter = 0
        #             while True:
        #                 try:
        #                     self.tcp_client.send(package_data_2_security(data))
        #                     confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
        #                     if confirm_data == 911000:
        #                         # print(data)
        #                         # print(len(data))
        #                         # print(counter)
        #                         counter += 1
        #                         timeout_counter = 0
        #                         break
        #                 except socket.timeout as e:
        #                     timeout_counter += 1
        #                     print(e.args)
        #                     print(traceback.format_exc())
        #                     print("大文件数据发送超时，尝试重新发送")
        #                     if timeout_counter == 5:
        #                         return