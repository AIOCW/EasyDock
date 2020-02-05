from entity.app_setting import AppSetting
from data_manager.app_setting_location import init_setting

import sqlite3


def init_database():
    database_name = "../db/EasyDock.db"

    # 创建app_info数据
    sql_app_info = '''CREATE TABLE IF NOT EXISTS AppInfo(
           id integer primary key not null ,
           name text not null,
           path text not null,
           icon_path text not null,
           icon_gray_path text not null);'''

    sql_app_setting = '''create table if not exists AppSetting(
            id integer not null,
            ip text not null,
            remove_ip text not null,
            port text not null,
            device_name text not null,
            file_local_save_name text not null,
            auto_open_image integer not null,
            auto_check_paste integer not null,
            use_rgb integer not null);
            '''

    conn = sqlite3.connect(database_name)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute(sql_app_info)
    c.execute(sql_app_setting)
    print("Table created successfully")
    conn.commit()
    conn.close()

def init_table_data_for_setting():
    app_setting = AppSetting("192.168.31.1", "192.168.31.1", "8080", "yaque-computer", "C:/Users/yaque/Desktop/PhoneFile/", 1, 1, 1)
    init_setting(app_setting)

if __name__ == "__main__":
    init_database()

