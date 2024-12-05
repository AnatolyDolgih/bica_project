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
        self.p_const = 0.03
        self.r_const = 0.1

        self.appraisals_state = np.zeros(self.space_size//2)
        self.feelings_state = np.zeros(self.space_size//2)
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

        self.appraisals_state = self.appraisals[:self.space_size//2] -  self.appraisals[self.space_size//2:]
        self.feelings_state = self.feelings[:self.space_size//2] -  self.feelings[self.space_size//2:]

    def get_appraisals(self):
        return self.appraisals

    def get_feelings(self):
        return self.feelings

    def get_appraisals_state(self):
        return self.appraisals_state

    def get_feelings_state(self):
        return self.feelings_state
