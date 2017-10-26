# encoding=utf-8
import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig(object):
    def __init__(self):
        fd = open(configPath)
        try:
            data = fd.read()
            # 移除 BOM
            if data[:3] == codecs.BOM_UTF8:
                data = data[3:]
                datafile = codecs.open(configPath, "w")
                datafile.write(data)
                datafile.close()
        finally:
            fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding="utf-8-sig")

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_be(self, name):
        value = self.cf.get("BROWSER", name)
        return value
