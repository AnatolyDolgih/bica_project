import os
import logging

log_folder = os.path.abspath("../logs/")
log_file = os.path.join(log_folder, "app_log.log")

def clearLog():
    for filename in os.listdir(log_folder):
        file_path = os.path.join(log_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

class Logger():
    def __init__(self, logger_name, log_file):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger_handler = logging.FileHandler(f"{log_file}", mode="a", encoding="utf-8")
        self.logger_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
        self.logger_handler.setFormatter(self.logger_formatter)
        self.logger.addHandler(self.logger_handler)

        self.logger.info(f"Testing the custom logger {logger_name}")

    def debug(self, msg): 
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def crtitcal(self, msg):
        self.logger.crtitcal(msg)