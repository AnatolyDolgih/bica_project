import math
import numpy as np
from oai_interface import Interface

class BaseMoralScheme:
    def __init__(self, base_intentions, changed_message = None, 
                 appraisals = None, feelings = None):
        # базисные вектора семантического пространства
        self.base_intentions = base_intentions

        # размер семантического пространства
        self.space_size = len(base_intentions)

        # константы для формул
        self.p_const = 0.1
        self.r_const = 0.1

        # Интерфейс для взаимодействия в openAI через прокси
        self.oai_interface = Interface()

        # векторы appraisals и feelings
        if appraisals is None:
            self.appraisals = np.zeros(self.space_size)
        else:
            self.appraisals = appraisals
        
        if feelings is None:
            self.feelings = np.empty(self.space_size)
            self.feelings.fill(0.5)
        else:
            self.feelings = feelings
    
    # расстояние между векторами
    def euc_dist(self, a, b):
        if len(a) != len(b):
            raise ValueError("Векторы должны иметь одинаковую длину")

        distance = math.sqrt(sum((a_i - b_i) ** 2 for a_i, b_i in zip(a, b)))
        return distance
    # ???
    def get_base_intentions(self):
        return self.base_intentions 

    def update_vectors(self, action):
        self.appraisals = (1 - self.r_const) * self.appraisals \
            + self.r_const * action
        self.feelings = (1 - self.p_const) * self.feelings \
            + self.p_const * (self.appraisals - self.feelings)

    def get_appraisals(self):
        return self.appraisals

    def get_feelings(self):
        return self.feelings

# class BaseMoralScheme():
#     def __init__(self, id, intentions = None):
#         # название моральной схемы
#         self.id = id

#         # const that can be changed further
#         self.p_const = 0.1 # const for appraisals
#         self.r_const = 0.1 # const for feelings
#         self.N_const = 5 # size of semantic spaces

#         # vector-intentions
#         self.intentions = intentions

#         # appraisals, feelings & action
#         self.appraisals = np.zeros(self.N_const)
#         self.feelings = np.zeros(self.N_const)
        
#         # threshold for dist
#         self.threshold = 0.25
        
#         # steps and time
#         self.max_steps = 100
#         self.step_count = 0
        
#         self.max_time = 2
#         # timer to exit when speaking more than max_time
#         # self.timer = threading.Timer(self.max_time, self.stop_timer)
#         # self.timer.start()

#         # interface to communicate with ChatGPT
#         self.interface = Interface()

#         # property that scheme is active
#         self.is_active = False

#     def get_id(self):
#         return self.id
    
#     # обновление appraisals и feelings
#     def update_vectors(self):
#         self.appraisals = (1 - self.r_const) * self.appraisals \
#             + self.r_const * self.action
#         self.feelings = (1 - self.p_const) * self.feelings \
#             + self.p_const * (self.appraisals - self.feelings)
#         return

#     # расчет расстояния между apparaisals и feelings
#     def dist(self):
#         return np.linalg.norm(self.appraisals, self.feelings)

#     # разложение входящей фразы по базовым интенциональностям
#     def add_action_vector(self, replic):
#         self.action = self.interface.get_composition(self.intentions, replic) 
#         return

#     # критерий перехода
#     # TODO: добавить время и количество шагов
#     def criteria(self):
#         if self.dist() < self.threshold:
#             return True
#         return False

#     def isActive(self):
#         return self.is_active    
                    
#     def update_scheme(self):
#         return False
