# encoding=utf-8
import cx_Oracle
import readConfig as readConfig
from Log import Log

log = Log(logger="DB")
logger = log.get_logger()
localReadConfig = readConfig.ReadConfig()


# noinspection PyGlobalUndefined
class MyDB(object):
    def __init__(self):
        global username, password, host, port, sid, config
        username = localReadConfig.get_db("username")
        password = localReadConfig.get_db("password")
        host = localReadConfig.get_db("host")
        port = localReadConfig.get_db("port")
        sid = localReadConfig.get_db("sid")
        self.db = None
        self.cursor = None

    def connectDB(self):
        try:
            tns = cx_Oracle.makedsn(host, port, sid)
            self.db = cx_Oracle.connect(username, password, tns)
            print("Connect DB successfully!")
        except Exception as ex:
            logger.error(str(ex))

    def closeDB(self):
        self.db.close()
        print("Database closed!")

    def query_by_one(self, sql, params=None):
        self.cursor = self.db.cursor()
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.prepare(sql)
            self.cursor.execute(None, params)
        self.cursor.close()
        self.db.commit()

    def query_by_many(self, sql, params):
        self.cursor = self.db.cursor()
        self.cursor.prepare(sql)
        self.cursor.executemany(None, params)
        self.cursor.close()
        self.db.commit()

    def get_all(self, sql, params=None):
        self.cursor = self.db.cursor()
        if params is None:
            self.cursor.execute(sql)
        else:
            self.cursor.prepare(sql)
            self.cursor.execute(None, params)
        value = self.cursor.fetchall()
        self.cursor.close()
        return value

    # def get_one(self, sql, params=None):
    #     if params is None:
    #         params = {}
    #     self.cursor = self.db.cursor()
    #     if len(params) > 0:
    #         self.cursor.prepare(sql)
    #         self.cursor.execute(None, params)
    #     else:
    #         self.cursor.execute(sql)
    #     value = self.cursor.fetchone()
    #     self.cursor.close()
    #     return value

    # def get_many(self, sql, number):
    #     self.cursor = self.db.cursor()
    #     self.cursor.execute(sql)
    #     value = self.cursor.fetchmany(number)
    #     self.cursor.close()
    #     return value

    # def get_all1(self, sql, arraysize):
    #     self.cursor = self.db.cursor()
    #     self.cursor.arraysize = arraysize
    #     self.cursor.execute(sql)
    #     value = self.cursor.fetchall()
    #     self.cursor.close()
    #     return value
