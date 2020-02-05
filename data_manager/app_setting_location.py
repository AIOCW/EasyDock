#!/usr/bin/python

import sqlite3
from entity.app_setting import AppSetting
from default_config import *

log_info = "app_setting_location.py"

def init_setting(app_setting):
    # print(app_setting.to_string())
    # 初始化使用INSERT 操作
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("{}即将进行数据插入操作".format(log_info))

    sql = '''insert into {} (
                id, ip, remove_ip, port, device_name, file_local_save_name, auto_open_image, auto_check_paste, 
                use_rgb)
                values (1, '{}', '{}', '{}', '{}', '{}', {}, {}, {});'''.format(
            APP_SETTING_TABLE_NAME,
            app_setting.ip,
            app_setting.remove_ip,
            app_setting.port,
            app_setting.device_name,
            app_setting.file_local_save_name,
            app_setting.auto_open_image,
            app_setting.auto_check_paste,
            app_setting.use_rgb
    )

    print(sql)

    c.execute(sql)

    conn.commit()
    print("{}初始化插入默认参数设置成功".format(log_info))
    conn.close()


def select_setting():
    # SELECT 操作
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("{}设置数据的查询开始".format(log_info))

    sql = '''select * from {};'''.format(APP_SETTING_TABLE_NAME)

    cursor = c.execute(sql)
    for coum in cursor:
        app_setting = AppSetting(coum[1], coum[2], coum[3], coum[4], coum[5], coum[6], coum[7], coum[8])
    print("{}查询成功，开始返回".format(log_info))
    conn.close()
    return app_setting


def update_setting(data, data_name):
    # UPDATE 操作
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("{}开始更新设置内容".format(log_info))

    sql = '''
            UPDATE {} set {} = '{}' where id=1;
    '''.format(APP_SETTING_TABLE_NAME, data_name, data)
    print(sql)
    c.execute(sql)
    conn.commit()
    print("{}Total number of rows updated :".format(log_info), conn.total_changes)


    print("{}成功更新数据".format(log_info))
    conn.close()