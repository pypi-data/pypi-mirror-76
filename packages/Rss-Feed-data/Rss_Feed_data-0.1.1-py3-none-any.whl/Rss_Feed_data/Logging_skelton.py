import logging
import datetime as dt
import os


class Config:
    """
        Class to create the logger object

        1.Success Logger
        2.Failure Logger

        ===================================================================
        """
    def __init__(self):
        self.CODE_DIR = os.getcwd()
        self.logger = None
        self.handler = None
        if not os.path.exists("logs"):
            os.mkdir("logs")

    def create_logger(self, logger_name, log_path):
        self.handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.handler.setFormatter(formatter)
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)
        return self.logger

    def create_success_logger(self):
        """

        This is used for creating success_logger which will be used to log the successful operation of
        the application

        """
        log_path1 = self.CODE_DIR + '/logs/success_logs_{}.log'.format(dt.datetime.now().strftime("%Y-%m-%d %H_%M"))
        success_logger = self.create_logger('success_logger', log_path1)
        return success_logger

    def create_failure_logger(self):
        """

        This is used for creating failure_logger which will be used to log the error operation of
        the application

        """
        log_path1 = self.CODE_DIR + '/logs/failure_logs_{}.log'.format(dt.datetime.now().strftime("%Y-%m-%d %H_%M"))
        failure_logger = self.create_logger('failure_logger', log_path1)
        return failure_logger
