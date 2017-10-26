# encoding=utf-8
import unittest
import paramunittest
from common import common
from common import configBE
from common.Log import Log as Log
from pageobjects.LoginIn_homepage import HomePage

log = Log(logger="testLogin")
login_xls = common.get_xls("userCase.xlsx", "login")


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, username, password, checkcode, result, msg):
        self.case_name = str(case_name)
        self.username = str(username)
        self.password = str(password)
        self.checkcode = str(checkcode)
        self.result = str(result)
        self.msg = str(msg)

    def setUp(self):
        """
        测试固件的setUp()的代码，主要是测试的前提准备工作
        """
        log.build_start_line(self.case_name)
        self.browse = configBE.BrowserEngine(self)
        self.driver = self.browse.open_browser(self)

    def testLogin(self):
        # 这里一定要test开头，把测试逻辑代码封装到一个test开头的方法里。
        self.homepage = HomePage(self.driver)
        self.homepage.send_username(self.username)  # 调用页面对象中的方法
        self.homepage.send_password(self.password)
        self.homepage.send_checkcode(self.checkcode)
        self.homepage.send_submit_btn()  # 调用页面对象类中的点击搜索按钮方法
        self.homepage.sleep(2)
        self.checkResult()  # 校验结果

    def tearDown(self):
        self.driver.quit()
        log.build_end_line(self.case_name)

    def checkResult(self):
        if self.result == '0':
            try:
                assert u'防盗登记系统' in self.homepage.get_page_title()
            except Exception:
                self.homepage.get_windows_img()  # 调用基类截图方法
                raise
        if self.result == '1':
            pass
