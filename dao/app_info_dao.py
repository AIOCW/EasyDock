from data_manager import app_info_location


def insert(app_info):
    app_info_location.insert(app_info)
    return True


def select():
    return app_info_location.select()


def delete(id):
    app_info_location.delete(id)
    return True