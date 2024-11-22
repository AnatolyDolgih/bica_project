import os
import threading
import numpy as np
from logger import Logger
from oai_interface import Interface

class BaseMoralScheme():
    def __init__(self, logger_name):
        log_file = os.path.join(os.path.abspath("../logs/"), "common_log.log")
        self.logger=Logger(logger_name, log_file)

        # const that can be changed further
        self.p_const = 0.1
        self.r_const = 0.1
        self.N_const = 5

        # appraisals & feelings
        self.appraisals = np.zeros(self.N_const)
        self.feelings = np.zeros(self.N_const)
        
        # steps and time
        self.max_steps = 100
        self.step_count = 0
        
        self.max_time = 2
        self.timer = threading.Timer(self.max_time, self.stop_timer)
        self.timer.start()

        # interface
        self.interface = Interface()
            
    def update_state(self, cur_impact):
        self.cur_state += cur_impact

    def stop_timer(self):
        self.logger.warning("Вышло время !!!")