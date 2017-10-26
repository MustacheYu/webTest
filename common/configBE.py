# encoding=utf-8
import os
from selenium import webdriver
import readConfig as readConfig
from Log import Log

log = Log(logger="BrowserEngine")
logger = log.get_logger()
localReadConfig = readConfig.ReadConfig()


# noinspection PyGlobalUndefined
class BrowserEngine(object):
    def __init__(self, driver):
        global browser, url
        browser = localReadConfig.get_be("browserName")
        url = localReadConfig.get_be("baseurl")
        self.chrome_driver_path = os.path.join(readConfig.proDir, "tools", "chromedriver.exe")
        self.ie_driver_path = os.path.join(readConfig.proDir, "tools", "IEDriverServer.exe")
        self.driver = driver

    def open_browser(self, driver):

        if browser == "Firefox":
            driver = webdriver.Firefox()
            logger.info("Starting firefox browser.")
        elif browser == "Chrome":
            driver = webdriver.Chrome(self.chrome_driver_path)
            logger.info("Starting Chrome browser.")
        elif browser == "IE":
            driver = webdriver.Ie(self.ie_driver_path)
            logger.info("Starting IE browser.")

        driver.get(url)
        logger.info("Open url: %s" % url)
        driver.maximize_window()
        logger.info("Maximize the current window.")
        driver.implicitly_wait(10)
        logger.info("Set implicitly wait 10 seconds.")
        return driver
