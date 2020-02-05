#!/usr/bin/python

import sqlite3
from entity.app_info import AppInfo
from default_config import *


def insert(app_info):
    # INSERT 操作
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("Opened database successfully")

    sql = '''insert into {} (
                id, name, path, icon_path, icon_gray_path)
                values ({}, '{}', '{}', '{}', '{}');'''.format(
            APP_INFO_TABLE_NAME,
            app_info.id,
            app_info.name,
            app_info.path,
            app_info.icon_path,
            app_info.icon_gray_path)

    c.execute(sql)

    conn.commit()
    print("Records created successfully")
    conn.close()


def select():
    # SELECT 操作
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("Opened database successfully")

    sql = '''select * from {};'''.format(APP_INFO_TABLE_NAME)

    cursor = c.execute(sql)

    app_info_list = []
    for row in cursor:
        app_info = AppInfo(row[0], row[1], row[2], row[3], row[4])
        app_info_list.append(app_info)

    print("Operation done successfully")
    conn.close()
    return app_info_list


def delete(id):
    # DELETE 操作
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("Opened database successfully")

    sql = '''delete from {} where id = {};'''.format(APP_INFO_TABLE_NAME, id)

    c.execute(sql)
    conn.commit()
    print("Total number of rows deleted :", conn.total_changes)
    print("Operation done successfully")
    conn.close()


def update():
    # UPDATE 操作
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print("Opened database successfully")

    c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
    conn.commit()
    print("Total number of rows updated :", conn.total_changes)

    cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
    for row in cursor:
       print("ID = ", row[0])
       print("NAME = ", row[1])
       print("ADDRESS = ", row[2])
       print("SALARY = ", row[3], "\n")

    print("Operation done successfully")
    conn.close()


if __name__ == "__main__":
    app_list = []
    for i in range(1):
        app = AppInfo(i, "QQ", "C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe", "appIcon/腾讯QQ.png", "appIcon/腾讯QQ_gray.png")
        app_list.append(app)
        insert(app)
    for app in select():
        print(app.id, app.name, app.path, app.icon_path, app.icon_gray_path)
    # delete(3)
    # for app in select():
    #     print(app.id, app.name, app.path, app.icon_path, app.icon_gray_path)