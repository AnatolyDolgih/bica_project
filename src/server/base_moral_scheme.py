import os
import threading
import numpy as np
from logger import Logger
from oai_interface import Interface

class BaseMoralScheme():
    def __init__(self, id, intentions = None):
        # id моральной схемы
        self.id = id

        # const that can be changed further
        self.p_const = 0.1 # const for appraisals
        self.r_const = 0.1 # const for feelings
        self.N_const = 5 # size of semantic spaces

        # vector-intentions
        self.intentions = intentions

        # appraisals, feelings & action
        self.appraisals = np.zeros(self.N_const)
        self.feelings = np.zeros(self.N_const)
        self.action = np.zeros(self.N_const)

        # threshold for dist
        self.threshold = 0.25
        
        # steps and time
        self.max_steps = 100
        self.step_count = 0
        
        self.max_time = 2
        # timer to exit when speaking more than max_time
        # self.timer = threading.Timer(self.max_time, self.stop_timer)
        # self.timer.start()

        # interface to communicate with ChatGPT
        self.interface = Interface()

        # property that scheme is active
        self.is_active = False

    def get_id(self):
        return self.id
    # обновление appraisals и feelings
    def update_vectors(self):
        self.appraisals = (1 - self.r_const) * self.appraisals \
            + self.r_const * self.action
        self.feelings = (1 - self.p_const) * self.feelings \
            + self.p_const * (self.appraisals - self.feelings)
        return

    # расчет расстояния между apparaisals и feelings
    def dist(self):
        return np.linalg.norm(self.appraisals, self.feelings)

    # разложение входящей фразы по базовым интенциональностям
    def add_action_vector(self, replic):
        self.action = self.interface.get_composition(self.intentions, replic) 
        return

    # критерий перехода
    # TODO: добавить время и количество шагов
    def criteria(self):
        if self.dist() < self.threshold:
            return True
        return False

    def isActive(self):
        return self.is_active    
                    
    def update_scheme(self):
        return False
