# coding:utf-8

import logging
from datetime import datetime
import threading
import os
import readConfig

class Log:
    def __init__(self):
        global logPath,resulePath,proDir
        proDir = readConfig.proDir
        resulePath = os.path.join(proDir,"result")

        # create result file if it doesn't exist
        if not os.path.exists(resulePath):
            os.mkdir(resulePath)

        # define test tesult file name by localtime
        logPath = os.path.join(resulePath,str(datetime.now().strftime("%Y%m%d%H%M%S")))

        # create test result file if it doesn't exist
        if not os.path.exists(logPath):
            os.mkdir(logPath)

        # define logger
        self.logger = logging.getLogger()

        # define log level
        self.logger.setLevel(logging.INFO)

        # define handler
        handler = logging.FileHandler(os.path.join(logPath,"output.log"))

        #define formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        # add handler
        self.logger.addHandler(handler)

class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():

        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log