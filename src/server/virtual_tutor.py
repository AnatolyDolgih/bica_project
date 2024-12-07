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
        self.logger_dialog = create_logger(f"dialog_logger_{self.client_id}", f"../../logs_dummy/{self.client_id}", "dialog.log")
        self.logger_essay = create_logger(f"essay_logger_{self.client_id}", f"../../logs_dummy/{self.client_id}", "essay.log")
        
        self.logger_dialog.info("This is dialog log")
        self.logger_essay.info("This is essay log")
        
    def generate_answer(self, replic):
        self.messages.append({"role": "user", "content": replic})
        tutor_response = self.oai_interface.get_dummy_replic(self.messages)
        return tutor_response

class VirtualTutor:
    def __init__(self, id):
        self.client_id = id
        self.logger_dialog = create_logger(f"dialog_logger_{self.client_id}", f"../../logs_moral/{self.client_id}", "dialog.log")
        self.logger_essay = create_logger(f"essay_logger_{self.client_id}", f"../../logs_moral/{self.client_id}", "essay.log")

        self.logger_dialog.info("This is dialog log")
        self.logger_essay.info("This is essay log")

        # список моральных схем
        self.ms_list = [BaseMoralScheme(hlp.first_space, hlp.from1to2, feelings=hlp.feelings1), 
                        BaseMoralScheme(hlp.second_space, hlp.from2to3, feelings=hlp.feelings2), 
                        BaseMoralScheme(hlp.third_space, hlp.from3to4, feelings=hlp.feelings3),
                        BaseMoralScheme(hlp.third_space, feelings=hlp.feelings4)]
        
        self.last_replic = ""
        self.prev_moral_id = 0
        self.cur_moral_id = 0
        self.messages = [ {"role": "assistant", "content": hlp.start_promt_dvt} ]
        self.schemes = [False, False, False, False]
        self.brain = [False, False, False, False]

    def generate_answer(self, replic):
        self.logger_dialog.warning(f'Сх: {self.schemes}') #Выводим состояние моральных схем
        self.logger_dialog.warning(f'Br: {self.brain}') #Выводим состояние моральных схем

        intents = self.ms_list[self.cur_moral_id].get_base_intentions()        
        action = self.ms_list[self.cur_moral_id].oai_interface.get_composition(intents, replic)
        if action is None:
            return "Не удалось связаться с сервером"
        self.logger_dialog.warning(action)
        self.ms_list[self.cur_moral_id].update_vectors(np.array(action))

        appr_state = self.ms_list[self.cur_moral_id].get_appraisals_state()
        feel_state = self.ms_list[self.cur_moral_id].get_feelings_state()
        dist = self.ms_list[self.cur_moral_id].euc_dist(appr_state, feel_state)

        self.logger_dialog.warning(f'appr:{self.ms_list[self.cur_moral_id].get_appraisals()}')
        self.logger_dialog.warning(f'feel:{self.ms_list[self.cur_moral_id].get_feelings()}')
        self.logger_dialog.warning(f'appr_state:{self.ms_list[self.cur_moral_id].get_appraisals_state()}')
        self.logger_dialog.warning(f'feel_state:{self.ms_list[self.cur_moral_id].get_feelings_state()}')

        diff = appr_state-feel_state

        self.logger_dialog.warning(f'diff: {diff}')

        self.prev_moral_id = self.cur_moral_id


        if self.cur_moral_id <=2:
            condition = self.ms_list[self.cur_moral_id].oai_interface.get_brain_status(self.messages, replic, self.cur_moral_id)

            self.logger_dialog.warning(f'cond: {condition}')

            if "да" in condition.lower():
                self.brain[self.cur_moral_id] = True
                self.cur_moral_id = min(self.cur_moral_id + 1, 3 )



        if dist < 0.25: #проверка на превосходство крит. точки
            self.schemes[self.cur_moral_id] = True #Для начала ставим статус текущей схемы в тру
            ##self.cur_moral_id = min(self.cur_moral_id + 1, 2 ) #переходим на след схему, 3 - это число сколько всего схем
        
        self.logger_dialog.warning(f'cur: {self.cur_moral_id}')
        self.logger_dialog.warning(f'prev: {self.prev_moral_id}')
            
        reply = self.ms_list[self.cur_moral_id].oai_interface.get_replic(replic, self.messages, intents, diff, self.prev_moral_id, self.cur_moral_id) #генерируем овтет бота
        self.messages.append({"role": "user", "content": replic}) #обновляем историю диалога
        self.messages.append({"role": "assistant", "content": reply}) #обновляем историю диалога       
        return reply 
