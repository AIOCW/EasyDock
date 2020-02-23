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
import traceback

from tools.net_tools import unpackage_data_2_security, package_data_2_security ,data2byte, byte2data
from tools.file_tools import get_file_inform, split_file, composite_file
from tools.md5 import getmd5

from mutil_file_send_thread import FileSendQThread

TAG = "tools_sockt_client:     "
buffsize = 1024


qmut_tool = QMutex() # 创建线程锁
class SocketQThread(QThread):
    my_signal = pyqtSignal(str)
    is_connection = False
    # tcp_client = socket(AF_INET, SOCK_STREAM)

    def __init__(self, app_setting):
        super(SocketQThread, self).__init__()
        self.setObjectName("NetThread")
        self.host = app_setting.ip
        self.port = app_setting.port
        self.device_name = app_setting.device_name
        self.file_local_save_name = app_setting.file_local_save_name
        self.is_send_heartbeat = True  # 1
        self.send_code = -1
        self.recv_code = -1

        self.return_type_flag = ''

        self.send_file_path = ''
        self.send_aim = ''

        self.text_message_aim_device = ''
        self.text_message = ''

    def run(self):
        self.start_net_fun()
        while True:
            if self.is_connection:
                print("{}可以连接到服务器".format(TAG))
                # 心跳保持工具
                if self.is_send_heartbeat:
                    qmut_tool.lock()
                    print('heartbeat')
                    self.heartbeat()
                    # self.my_signal.emit("2" + "+0~^D" + self.heartbeat())
                    self.sleep(3)
                    print("当前recv_code{}".format(self.recv_code))
                    qmut_tool.unlock()

                # 获取已连接服务端的客户端数量
                elif self.send_code == 1001:
                    qmut_tool.lock()
                    self.tcp_client.send(package_data_2_security(data2byte(1001)))
                    confirm_code_buffer = self.tcp_client.recv(4)
                    confirm_code = byte2data(unpackage_data_2_security(confirm_code_buffer))
                    if confirm_code == 1001:
                        message_len_buffer = self.tcp_client.recv(4)
                        message_len = byte2data(unpackage_data_2_security(message_len_buffer))
                        message_buffer = self.tcp_client.recv(message_len)
                        message = unpackage_data_2_security(message_buffer)
                        self.tcp_client.send(package_data_2_security(data2byte(1001)))
                        message = self.return_type_flag + "1001" + "+0~^D" + message.decode('utf-8')
                        self.my_signal.emit(message)

                        self.send_code = -1
                        self.is_send_heartbeat = True
                    else:
                        print("获取数据失败")
                    qmut_tool.unlock()
                    print("end 1001================")

                # 发送文本消息
                elif self.send_code == 1011:
                    self.send_text_message()

                # 发送文件
                elif self.send_code == 1100:
                    print(self.send_file_path + "    in tools")
                    self.send_file()

                # 接收
                # 接收文本
                elif self.recv_code == 91011:
                    self.rece_text_message()

                # 接收小文件
                if self.recv_code == 91100:
                    print("接收小文件{}".format(self.recv_code))
                    self.recv_code = -1
                    self.recv_file()
                    self.is_send_heartbeat = True
            # 网络错误处理
            else:
                print("网络错误")
                self.start_net_fun()
                time.sleep(10)

    def get_other_client_data_api(self, file_path, type_flag):
        self.return_type_flag = type_flag
        self.send_code = 1001
        self.is_send_heartbeat = False
        self.send_file_path = file_path

    def send_text_message_api(self, text_message, aim_device):
        self.text_message = text_message
        self.text_message_aim_device = aim_device
        self.send_code = 1011
        self.is_send_heartbeat = False

    def send_text_message(self):
        try:
            self.tcp_client.send(package_data_2_security(data2byte(1011)))
            print('向服务端发送文本消息')
            json_message = {
                'client_name': self.text_message_aim_device,
                'security_md5_text': self.text_message
            }
            json_message = json.dumps(json_message)
            json_message_buffer = json_message.encode('utf-8')
            json_message_buffer = package_data_2_security(json_message_buffer)
            json_message_len_buffer = data2byte(len(json_message_buffer))
            json_message_len_buffer = package_data_2_security(json_message_len_buffer)
            self.tcp_client.send(json_message_len_buffer)  # 这里是4个字节
            self.tcp_client.send(json_message_buffer)  # 发送报头的内容
            success_code_buffer = self.tcp_client.recv(4)
            success_code = byte2data(unpackage_data_2_security(success_code_buffer))
            if success_code == 1011:
                self.is_send_heartbeat = True
                self.send_code = -1
        except Exception as e:
            print(e.args)
            print(traceback.format_exc())
            print("Error{}, is_connection={}".format("网络错误，重置网络标识，启动服务器链接监测", self.is_connection))

    def rece_text_message(self):
        confirm_code_buffer = self.tcp_client.recv(4)
        confirm_code = byte2data(unpackage_data_2_security(confirm_code_buffer))
        if confirm_code == 1011:
            json_data_len_buffer = self.tcp_client.recv(4)
            json_data_len = byte2data(unpackage_data_2_security(json_data_len_buffer))
            json_data_buffer = self.tcp_client.recv(json_data_len)
            json_data = unpackage_data_2_security(json_data_buffer)
            json_data = json_data.decode('utf-8')
            json_data = json.loads(json_data)

            text_message = "91011" + "+0~^D" + json_data['security_md5_text']
            self.my_signal.emit(text_message)

            self.recv_code = -1
            self.is_send_heartbeat = True

    # 文件发送的入口
    def send_file_api(self, send_aim):
        self.send_aim = send_aim
        self.send_code = 1100
        self.is_send_heartbeat = False

    # 发送文件
    def send_file(self):
        head_info_len, head_info, file_size = get_file_inform(self.send_file_path, self.send_aim)
        print(head_info)
        if head_info_len > 0:
            if file_size < 512000:
                try:
                    self.tcp_client.send(package_data_2_security(data2byte(1100)))

                    confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
                    if confirm_data == 91100:
                        head_info_buffer = head_info.encode('utf-8')
                        head_info_buffer = package_data_2_security(head_info_buffer)
                        head_info_len_buffer = data2byte(len(head_info_buffer))
                        head_info_len_buffer = package_data_2_security(head_info_len_buffer)
                        self.tcp_client.send(head_info_len_buffer)  # 这里是4个字节
                        self.tcp_client.send(head_info_buffer)  # 发送报头的内容

                        s = time.time()
                        counter = 0
                        with open(self.send_file_path, 'rb') as sf:
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
                                        if confirm_data == 91100:
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
                                        print("文件数据发送超时，尝试重新发送")
                                        if timeout_counter == 5:
                                            return
                                # break
                        success_code_buffer = self.tcp_client.recv(4)
                        success_code = byte2data(unpackage_data_2_security(success_code_buffer))
                        if success_code == 91100:
                            self.is_send_heartbeat = True
                            self.send_code = -1
                            print("文件发送成功, 一共耗时 {}".format(time.time() - s))
                            tip_message = "91100" + "+0~^D" + "文件发送成功"
                            self.my_signal.emit(tip_message)
                        else:
                            print("文件发送失败")
                except Exception as e:
                    print(e.args)
                    print(traceback.format_exc())
            else:
                try:
                    self.tcp_client.send(package_data_2_security(data2byte(11004)))
                    confirm_data = byte2data(unpackage_data_2_security(self.tcp_client.recv(4)))
                    if confirm_data == 911004:
                        head_info_buffer = head_info.encode('utf-8')
                        head_info_buffer = package_data_2_security(head_info_buffer)
                        head_info_len_buffer = data2byte(len(head_info_buffer))
                        head_info_len_buffer = package_data_2_security(head_info_len_buffer)
                        self.tcp_client.send(head_info_len_buffer)  # 这里是4个字节
                        self.tcp_client.send(head_info_buffer)  # 发送报头的内容
                except Exception as e:
                    print(e.args)
                    print("============")
                    print(traceback.format_exc())
                for one_file_path in split_file(self.send_file_path, 5):
                    file_send_thread = FileSendQThread(one_file_path, self.host, self.port, self.send_aim)
                    file_send_thread.start()
        self.send_code = -1
        self.send_file_path = ''
        self.send_aim = ''
        self.is_send_heartbeat = True

    def recv_file(self):
        print("进入小文件接收函数")
        self.tcp_client.send(package_data_2_security(data2byte(91100)))
        # 接受客户端介绍信息的长度
        json_data_len_buffer = self.tcp_client.recv(4)
        json_data_len_buffer_unpackage = unpackage_data_2_security(json_data_len_buffer)
        json_data_len = byte2data(json_data_len_buffer_unpackage)

        # 接受介绍信息的内容
        json_data_buffer = self.tcp_client.recv(json_data_len)
        json_data_buffer_unpackage = unpackage_data_2_security(json_data_buffer)
        # 将介绍信息的内容反序列化
        json_data = json.loads(json_data_buffer_unpackage.decode('utf-8'))
        print("本次介绍信息的内容为：{}".format(json_data))
        print("本次file长度为：{}".format(json_data["filesize"]))

        # #   文件接收
        print("进入接收区")
        filename = json_data['filename']
        filesize = json_data['filesize']
        filepath = json_data['filepath']
        aim_device = json_data['aim_device']
        md5 = json_data['md5']

        recv_len = 0

        with open(self.file_local_save_name + filename, 'wb') as sf:
            now_data_number = 0;
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
                            sf.write(file_buffer)
                        else:
                            end_size = filesize - recv_len
                            recv_len += end_size
                            sf.write(file_buffer[0:end_size])
                        self.tcp_client.send(package_data_2_security(data2byte(91100)))
                        now_data_number += 1
                    else:
                        continue
                else:
                    continue
        new_file_md5 = getmd5(self.file_local_save_name + filename)
        if new_file_md5 == md5:
            print("new_file_md5 {}, md5 {}".format(new_file_md5, md5))
            print("文件接收成功")
            tip_message = "91100" + "+0~^D" + "文件接收成功"
            self.my_signal.emit(tip_message)

    # 心跳处理段
    def heartbeat(self):
        print("进入心跳包发送阶段")
        success_code = 0
        try:
            self.tcp_client.send(package_data_2_security(data2byte(1010)))
            success_code_buffer = self.tcp_client.recv(4)
            success_code = byte2data(unpackage_data_2_security(success_code_buffer))
            if success_code == 1010:
                print("心跳包接收的是{}".format(success_code))
        except ValueError:
            print("值错误{}，进行服务重连或服务切换".format(ValueError))
            self.is_connection = False
        except Exception as e:
            print(e.args)
            print("==============")
            print(traceback.format_exc())
            print("{}".format("心跳保持出现问题，进行服务重连或切换"))
            self.is_connection = False
        if success_code == 1010:
            status = '在线9'
        elif success_code == 91011:
            status = '有文本信息'
            self.recv_code = 91011
            self.is_send_heartbeat = False
            return status
        elif success_code == 91100:
            status = '文件接收中。。。'
            self.recv_code = 91100
            self.is_send_heartbeat = False
            return status
        elif success_code == 9110040:
            status = '在线9'
            print("服务器成功接收发送的大文件，服务器计算md5值相同")
            tip_message = "91100" + "+0~^D" + "文件发送成功"
            self.my_signal.emit(tip_message)
        elif success_code == 4:
            status = '接收其它设备信息'
            self.is_send_heartbeat = False
            self.recv_code = 4
            return status
        else:
            status = '下线'
        return status

    # 开始连接服务器段
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
            json_message_buffer = json_message.encode('utf-8')
            json_message_buffer = package_data_2_security(json_message_buffer)

            self.tcp_client.send(package_data_2_security(data2byte(1000)))
            json_message_len_buffer = data2byte(len(json_message_buffer))
            json_message_len_buffer = package_data_2_security(json_message_len_buffer)
            self.tcp_client.send(json_message_len_buffer)  # 这里是4个字节
            self.tcp_client.send(json_message_buffer)  # 发送报头的内容
            success_code_buffer = self.tcp_client.recv(4)
            success_code = byte2data(unpackage_data_2_security(success_code_buffer))
            if success_code == 1000:
                self.is_connection = True
        except:
            self.is_connection = False
            print("Error{}, is_connection={}".format("网络错误，重置网络标识，启动服务器链接监测", self.is_connection))
