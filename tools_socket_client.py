#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-21 下午8:32
# @Author  : Yaque
# @File    : server_socket_文件客户端.py
# @Software: PyCharm

import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

from socket import *
import os
import json
import struct
import time


TAG = "tools_sockt_client:     "
buffsize = 1024


class SocketQThread(QThread):
    my_signal = pyqtSignal(str)
    is_connection = False
    tcp_client = socket(AF_INET, SOCK_STREAM)

    def __init__(self, app_setting):
        super(SocketQThread, self).__init__()
        self.host = app_setting.ip
        self.port = app_setting.port
        self.device_name = app_setting.device_name
        self.file_local_save_name = app_setting.file_local_save_name
        self.is_send_heartbeat = True  # 1
        self.send_code = -1
        self.recv_code = -1

        self.send_file_path = ''
        self.send_aim = ''

    def run(self):
        self.start_net_fun()
        while True:
            if self.is_connection:
                print("{}可以连接到服务器".format(TAG))
                # 心跳保持工具
                if self.is_send_heartbeat:
                    print('heartbeat')
                    self.my_signal.emit("2" + "+0~^D" + self.heartbeat())
                    self.sleep(1)
                    print("当前recv_code{}".format(self.recv_code))
                # 发送文件
                elif self.send_code == 1:
                    print(self.send_file_path + "    in tools")
                    #   判断文件是否存在
                    head_info_len, head_info = self.opera_file(self.send_file_path)
                    print(head_info)
                    self.tcp_client.send(struct.pack('i', 1))
                    self.tcp_client.send(head_info_len)  # 这里是4个字节
                    self.tcp_client.send(head_info.encode('utf-8'))  # 发送报头的内容
                    self.send_real_file(self.tcp_client, self.send_file_path)
                    # 确认是否成功
                    if struct.unpack('i', self.tcp_client.recv(4))[0] == 8:
                        print("发送成功：{}".format(8))
                    else:
                        print("发送失败")
                    self.send_code = -1
                    self.send_file_path = ''
                    self.send_aim = ''
                    self.is_send_heartbeat = True
                # 发送文字
                elif self.send_code == 3:
                    pass
                    # 发送文字
                    # send_file("")
                # 获取已连接服务端的客户端数量
                elif self.send_code == 11:
                    self.tcp_client.send(struct.pack('i', 11))
                    message_len = struct.unpack('i', self.tcp_client.recv(4))[0]
                    message = self.tcp_client.recv(message_len)
                    message = "1" + "+0~^D" + message.decode('utf-8')
                    self.my_signal.emit(message)

                    self.send_code = -1
                    self.is_send_heartbeat = True
                    # 发送文字
                    # send_file("")

                # 接收文件
                if self.recv_code == 1:
                    print("他人传输的进入文件接收{}".format(self.recv_code))
                    self.recv_code = -1
                    self.recv_file()
                    self.is_send_heartbeat = True
                elif self.recv_code == 4:
                    tip_message_len = struct.unpack('i', self.tcp_client.recv(4))[0]
                    tip_message = self.tcp_client.recv(tip_message_len)
                    tip_message = "4" + "+0~^D" + tip_message.decode('utf-8')
                    self.my_signal.emit(tip_message)

                    self.recv_code = -1
                    self.is_send_heartbeat = True
            else:
                print("网络错误")
                self.start_net_fun()
                time.sleep(10)

    def opera_file(self, filename):
        '''对报头进行打包'''
        filesize_bytes = os.path.getsize(filename)
        head_dir = {
            'filename': filename.split("/")[-1],
            'filesize': filesize_bytes,
            'filepath': 'file/',
            'aim_device': self.send_aim
        }
        head_info = json.dumps(head_dir)
        head_info_len = struct.pack('i', len(head_info))
        print(head_info_len)
        print(len(head_info))
        return head_info_len, head_info

    def get_other_client_data(self, file_path):
        self.send_code = 11
        self.is_send_heartbeat = False
        self.send_file_path = file_path

    # 给主线程调用的入口
    def send_file(self, send_aim):
        self.send_aim = send_aim
        self.send_code = 1
        self.is_send_heartbeat = False

    def send_real_file(self, conn, filename):
        '''发送真是文件'''
        with open(filename, 'rb')as f:
            conn.sendall(f.read())

        print('发送成功')

    def recv_file(self):
        print("进入文件接收函数")
        struct_len = self.tcp_client.recv(4)  #  接受报头的长度
        struct_info_len = struct.unpack('i',struct_len)[0]  #   解析得到报头信息的长度
        head_info = self.tcp_client.recv(struct_info_len)   #    接受报头的内容
        head_dir = json.loads(head_info.decode('utf-8'))              #   将报头的内容反序列化
        # #   文件接收
        self.recv_real_file(head_dir, self.tcp_client)

    def recv_real_file(self, head_dir, tcp_client):
        print("进入接收区")
        filename = head_dir['filename']
        filesize = head_dir['filesize']
        filepath = head_dir['filepath']
        aim_device = head_dir['aim_device']
        recv_len = 0
        recv_mesg = b''
        f = open(self.file_local_save_name + filename, 'wb')
        while recv_len < filesize:
            if filesize - recv_len > buffsize:
                recv_mesg = tcp_client.recv(buffsize)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
            else:
                recv_mesg = tcp_client.recv(filesize - recv_len)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
        f.close()
        print('文件接收完成')

    def heartbeat(self):
        print("进入心跳包发送阶段")
        order = -1
        try:
            self.tcp_client.send(struct.pack('i', 2))
            order = struct.unpack('i', self.tcp_client.recv(4))[0]
            print("心跳包接收的是{}".format(order))
        except ValueError:
            print("值错误{}，进行服务重连或服务切换".format(ValueError))
            self.is_connection = False
        except:
            print("{}".format("心跳保持出现问题，进行服务重连或切换"))
            self.is_connection = False
        if order == 9:
            status = '在线9'

        elif order == 1:
            status = '文件接收中。。。'
            self.recv_code = 1
            self.is_send_heartbeat = False
            return status
        elif order == 4:
            status = '接收其它设备信息'
            self.is_send_heartbeat = False
            self.recv_code = 4
            return status
        else:
            status = '下线'
        return status

    def start_net_fun(self):
        print(self.host, self.port)
        self.tcp_client = socket(AF_INET, SOCK_STREAM)
        ip_port = ((self.host, int(self.port)))
        self.tcp_client.connect_ex(ip_port)
        try:
            print('向服务端发送本机信息')
            json_message = {
                'client_name': self.device_name
            }
            json_message = json.dumps(json_message)
            json_message_len = struct.pack('i', len(json_message))
            print(json_message_len)
            self.tcp_client.send(struct.pack('i', 0))
            self.tcp_client.send(json_message_len)  # 这里是4个字节
            self.tcp_client.send(json_message.encode('utf-8'))  # 发送报头的内容
            self.is_connection = True
        except:
            self.is_connection = False
            print("Error{}, is_connection={}".format("网络错误，重置网络标识，启动服务器链接监测", self.is_connection))
