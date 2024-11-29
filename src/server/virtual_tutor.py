import numpy as np
import helper as hlp
import logging
from pathlib import Path
import os
from base_moral_scheme import BaseMoralScheme
from oai_interface import Interface

def create_logger(logger_name, log_dir, log_file):
    Path(log_dir).mkdir(parents=True, exist_ok=True)    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(log_dir, log_file), mode='w', encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

class DummyVirtualTutor:
    def __init__(self, id):
        self.client_id = id
        self.messages = [ {"role": "system", "content": hlp.start_promt_dvt} ]
        self.oai_interface = Interface()
        self.logger_dialog = create_logger(f"dialog_logger_{self.client_id}", f"../../logs/{self.client_id}", "dialog.log")
        self.logger_essay = create_logger(f"essay_logger_{self.client_id}", f"../../logs/{self.client_id}", "essay.log")
        
        self.logger_dialog.info("This is dialog log")
        self.logger_essay.info("This is essay log")
        print("ctor")

    def generate_answer(self, replic):
        self.messages.append({"role": "user", "content": replic})
        tutor_response = self.oai_interface.get_dummy_replic(self.messages)
        return tutor_response

class VirtualTutor:
    def __init__(self):
        # список моральных схем
        self.ms_list = [BaseMoralScheme(hlp.first_space, hlp.from1to2), 
                        BaseMoralScheme(hlp.second_space, hlp.from2to3), 
                        BaseMoralScheme(hlp.third_space)]
        
        self.last_replic = ""
        self.prev_moral_id = 0
        self.cur_moral_id = 0
        self.messages = [ {"role": "assistant", "content": hlp.start_promt} ]
        self.schemes = [False, False, False]

    def generate_answer(self, replic):
        print(f'Сх: {self.schemes}') #Выводим состояние моральных схем
        intents = self.ms_list[self.cur_moral_id].get_base_intentions()        
        action = self.ms_list[self.cur_moral_id].oai_interface.get_composition(intents, replic)
        self.ms_list[self.cur_moral_id].update_vectors(np.array(action))

        appr = self.ms_list[self.cur_moral_id].get_appraisals()
        feel = self.ms_list[self.cur_moral_id].get_feelings()
        dist = self.ms_list[self.cur_moral_id].euc_dist(appr, feel)

        self.prev_moral_id = self.cur_moral_id
        if dist < 0.25: #проверка на превосходство крит. точки
            self.schemes[self.cur_moral_id] = True #Для начала ставим статус текущей схемы в тру
            self.cur_moral_id = min(self.cur_moral_id + 1, 2 ) #переходим на след схему, 3 - это число сколько всего схем
        reply = self.ms_list[self.cur_moral_id].oai_interface.get_replic(replic, self.messages, intents, feel, self.prev_moral_id, self.cur_moral_id) #генерируем овтет бота
        self.messages.append({"role": "user", "content": replic}) #обновляем историю диалога
        self.messages.append({"role": "assistant", "content": reply}) #обновляем историю диалога       
        return reply


# class VirtualTutor():
#     def __init__(self):
#         # Моральные схемы: хранятся списоком, пока будет 4 штуки
#         self.moral_list = [bms.BaseMoralScheme(x, hlp.ms_1_greetings) for x in range(4)]
#         self.cur_ms = self.moral_list[0]

#         logger_name = "virtual_tutor"
#         self.logger = logging.getLogger(logger_name)
#         self.logger.setLevel(logging.INFO)

#         self.handler = logging.FileHandler(f"{logger_name}.log", mode='w')
#         self.formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

#         self.handler.setFormatter(self.formatter)
#         self.logger.addHandler(self.handler)
#         self.logger.info(f"test logger {logger_name}")
#         string = os.environ["TUTOR_FORT"]
#         self.logger.info(f"TUTOR_FORT: {string}")

#     def generate_answer(self, replic):
#         self.logger.info(f"User: {replic}")
        
#         # добавили в моральную схему разложение фразы по базисным 
#         # векторам семантического пространства 
#         self.cur_ms.add_action_vector(replic)
        
#         # пересчитали значение appraisals и feelings
#         self.cur_ms.update_vectors()


#         reply = self.cur_ms.generate_answer()
#         if self.cur_ms.criteria():
#             # переход на другую моральную схему
#             self.cur_ms = self.cur_ms
        
#         return reply

#     def generate_emotion(self):
#         pass


# if __name__ == "__main__":
#     actor = VirtualTutor()