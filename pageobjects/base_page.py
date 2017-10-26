# encoding=utf-8
import os
import time
from selenium.common.exceptions import NoSuchElementException
from common.Log import Log as Log
from common import common

log = Log(logger="BasePage")
logger = log.get_logger()


def ele_pathvalue(page_name, element_name):
    element_dict = common.get_xml_dict(page_name, element_name)
    path_value = element_dict.get("pathvalue")
    return path_value


class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法到这个类
    """

    def __init__(self, driver):
        self.driver = driver

    # 浏览器前进操作
    def forward(self):
        self.driver.forward()
        logger.info("Click forward on current page.")

    # 浏览器后退操作
    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    # 点击关闭当前窗口
    def close(self):
        try:
            self.driver.close()
            logger.info("Closing and quit the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)

    # 获得网页标题
    def get_page_title(self):
        logger.info("Current page title is %s" % self.driver.title)
        return self.driver.title

    # 硬性等待
    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)

    # 定位元素方法
    def find_element(self, selector):
        """
         这个地方为什么是根据=>来切割字符串，请看页面里定位元素的方法
         submit_btn = "id=>su"
         login_lnk = "xpath => //*[@id='u1']/a[7]"  # 百度首页登录链接定位
         如果采用等号，结果很多xpath表达式中包含一个=，这样会造成切割不准确，影响元素定位
        :param selector:
        :return: element
        """
        element = ''
        selector_by = selector.split('=>')[0].lower()
        selector_value = selector.split('=>')[1].lower()

        if selector_by == 'id':
            try:
                element = self.driver.find_element_by_id(selector_value)
                logger.info("Had find the element successful "
                            "by %s value: %s " % (selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
        elif selector_by == 'name':
            try:
                element = self.driver.find_element_by_name(selector_value)
                logger.info("Had find the element successful "
                            "by %s value: %s " % (selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
        elif selector_by == 'class_name':
            try:
                element = self.driver.find_element_by_class_name(selector_value)
                logger.info("Had find the element successful "
                            "by %s value: %s " % (selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
        elif selector_by == 'link_text':
            try:
                element = self.driver.find_element_by_link_text(selector_value)
                logger.info("Had find the element successful "
                            "by %s value: %s " % (selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
        elif selector_by == 'partial_link_text':
            try:
                element = self.driver.find_element_by_partial_link_text(selector_value)
                logger.info("Had find the element successful "
                            "by %s value: %s " % (selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
        elif selector_by == 'tag_name':
            try:
                element = self.driver.find_element_by_tag_name(selector_value)
                logger.info("Had find the element successful "
                            "by %s value: %s " % (selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
        elif selector_by == 'xpath':
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                logger.info("Had find the element successful "
                            "by %s value: %s " % (selector_by, selector_value))
            except NoSuchElementException as e:
                logger.error("NoSuchElementException: %s" % e)
        elif selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    # 输入
    def type(self, page_name, element_name, text):
        path_value = ele_pathvalue(page_name, element_name)
        el = self.find_element(path_value)
        el.clear()
        try:
            el.send_keys(text)
            logger.info("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)

    # 清除文本框
    def clear(self, page_name, element_name):
        path_value = ele_pathvalue(page_name, element_name)
        el = self.find_element(path_value)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)

    # 点击元素
    def click(self, page_name, element_name):
        path_value = ele_pathvalue(page_name, element_name)
        el = self.find_element(path_value)
        try:
            el.click()
            logger.info("The element was clicked.")
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

# ****************************** screenshot ********************************
    # 保存图片
    def get_windows_img(self):
        """
        在这里我们把file_path这个参数写死，直接保存到我们项目根目录的一个文件夹.\Screenshots下
        """
        report_path = log.get_result_path()
        screenshots_path = os.path.join(report_path, "screenshots")
        if not os.path.exists(screenshots_path):
            os.mkdir(screenshots_path)
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + '.png'
        screen_name = os.path.join(screenshots_path, rq)
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /screenshots")
            print (u"用例结果截图路径:%s" % screen_name)
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
