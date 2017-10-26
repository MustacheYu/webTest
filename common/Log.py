# encoding=utf-8
import os
import logging
from datetime import datetime
import readConfig as readConfig


# noinspection PyGlobalUndefined
class Log(object):
    def __init__(self, logger):
        global proDir, resultPath, logPath
        proDir = readConfig.proDir
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于输出到日志文件
        fh = logging.FileHandler(os.path.join(logPath, "output.log"))
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def build_start_line(self, case_name):
        self.logger.info("--------" + case_name + " START--------")

    def build_end_line(self, case_name):
        self.logger.info("--------" + case_name + " END--------")

    def get_report_path(self):
        report_path = os.path.join(logPath, "report.html")
        return report_path

    def get_result_path(self):
        return logPath