import base_moral_scheme as bms
import logger as log
import os
import helper as hlp

class VirualTutor():
    def __init__(self):
        # Моральные схемы: хранятся списоком, пока будет 4 штуки
        self.moral_list = [bms.BaseMoralScheme(x, hlp.ms_1_greetings) for x in range(4)]
        self.cur_ms = self.moral_list[0]

    def generate_answer(self, replic):
        # добавили реплики в моральную схему и посчитали ее разложение 
        # по векторам интенциональностей
        self.cur_ms.add_action_vector(replic)
        
        # пересчитали значение appraisals и feelings
        self.cur_ms.update_vectors()

        reply = self.cur_ms.generate_answer()
        if self.cur_ms.criteria():
            # переход на другую моральную схему
            self.cur_ms = self.cur_ms
        
        return reply

    def generate_emotion(self):
        pass