class AppSetting(object):
    ip = ""
    remove_ip = ""
    port = ""
    device_name = ""
    file_local_save_name = ""
    auto_open_image = ""
    auto_check_paste = ""
    use_rgb = ""

    def __init__(self, ip, remove_ip, port, device_name, file_local_save_name, auto_open_image, auto_check_paste, use_rgb):
        self.ip = ip
        self.remove_ip = remove_ip
        self.port = port
        self.device_name = device_name
        self.file_local_save_name = file_local_save_name
        self.auto_open_image = auto_open_image
        self.auto_check_paste = auto_check_paste
        self.use_rgb = use_rgb

    def set_ip(self, ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def set_remove_ip(self, remove_ip):
        self.remove_ip = remove_ip

    def get_remove_ip(self):
        return self.remove_ip

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    def set_device_name(self, device_name):
        self.device_name = device_name

    def get_device_name(self):
        return self.device_name

    def set_file_local_save_name(self, file_local_save_name):
        self.file_local_save_name = file_local_save_name

    def get_file_local_save_name(self):
        return self.file_local_save_name

    def set_auto_open_image(self, auto_open_image):
        self.auto_open_image = auto_open_image

    def get_auto_open_image(self):
        return self.auto_open_image

    def set_auto_check_paste(self, auto_check_paste):
        self.auto_check_paste = auto_check_paste

    def get_auto_check_paste(self):
        return self.auto_check_paste

    def set_use_rgb(self, use_rgb):
        self.use_rgb = use_rgb

    def get_use_rgb(self):
        return self.use_rgb

    def to_string(self):
        print("ip, {} remove_ip, {} port, {} device_name, {} file_local_save_name, {} auto_open_image, {} auto_check_paste, {}\t" +
              "use_rgb {}".format(
            self.ip, self.remove_ip, self.port, self.device_name, self.file_local_save_name, self.auto_open_image, self.auto_check_paste,
                  self.use_rgb
        ))
