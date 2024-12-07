import numpy as np
import re
import requests
import json
import helper as hlp


class Interface:
    def __init__(self):
        config = hlp.load_config()
        self.token = config["auth"]["token"]
        
        self.header = {
            'Authorization': "Bearer x_cTiM9n_TLr80E85jjr4fSm4OfTTL8m3GyG_UOvoRLf7ajZDKvpEMgTDsQtacRwjoniI3qfaUKpJ-2lOEFY1g"
        }
        self.url = 'https://www.bicaai2023.org/openai/v1/chat/completions'

    def clear_intetions(self, reply):
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", reply)
        numbers = [float(num) if '.' in num else int(num) for num in numbers]
        return(numbers)

    def get_composition(self, intents_dict, fraze):
        cat_str = ', '.join(intents_dict.values())
        num = len(intents_dict.values())
        string = f'''
                Ты механизм по определению интенций в речи человека, связанных с его поведением 
                в различных социальных ситуациях.
                Твоей основной задачей является определить вероятность содержания каждой интенции 
                из сказанного предложения от 0 до 1. В твоем распоряжении только {num} 
                интенсиональностей для угадывания (они перечислены через запятую):
                {cat_str} Вероятность - число от 0 до 1, где 0 - интенция не содержится совсем, 
                а 1 - содержится точно. Используй интенции только из указанного списка! 
                Выведи {num} значений вероятности каждой интенциональности в фразе:  
                "{fraze}"
                Выведи только значения через запятую
        '''
        body = {
            'model': 'gpt-4o',
            'messages': [
                {
                    'role': 'assistant',
                    'content': string
                }
            ]
        }

        response = requests.post(url=self.url, headers=self.header, json=body)
        if response.ok:
            reply = json.loads(response.json())["choices"][0]["message"]["content"]
        else:
            reply = None
        return reply

    def get_replic(self, last_message, messages, intens_dict, feelings, 
                   prev_scheme, current_scheme):
       
        rlt = [(intens_dict[i if val > -0.05 else -i], val) for i, val in enumerate(feelings, start=1)]
        student_profile = '''Характеристика студента: \n'''

        # Перечисляем элементы
        for idx, (dict_value, list_value) in enumerate(rlt, start=1):
            fnt = f"Студент {dict_value}\n"
            student_profile += fnt
   
    
        for idx, (dict_value, list_value) in enumerate(rlt, start=1):
            if list_value < -0.05:
                mov = f"Студент оказался {dict_value}. \
                    Необходимо окрасить свой ответ так, чтобы это поспособствовало \
                    положительной смене этой характеристики"   
                student_profile += mov

        changed_message = f'''Последняя реплика человека:{last_message}.
            Сгенерируй фразу - ответ на последнюю реплику человека
            Фраза должна быть адекватным и логичным ответом к последней реплике человека.
            Фраза должна быть уместной в контексте всей истории диалога.
            Фраза должна быть не длинне 50 слов.
            Фраза не должна содержать никакой информации об этапах диалога
            Выведи только новую реплику.
            Ты должен поменять свой ответ с учетом характеристики студента: {student_profile}
            Параметры по переходам между этапами:
            '''

        if current_scheme-prev_scheme == 1 and current_scheme == 2:
            changed_message =  changed_message + hlp.from1to2 
        elif current_scheme-prev_scheme == 2 and current_scheme == 3:
            changed_message =  changed_message + hlp.from2to3
        elif current_scheme-prev_scheme == 3 and current_scheme == 4:
            changed_message =  changed_message + hlp.from3to4
        elif current_scheme == prev_scheme:
            changed_message =  changed_message + \
                f"Вы находитесь на {current_scheme+1} этапе. Переходить пока не нужно" 

        messages_opt = list(messages)
        messages_opt.append({"role": "user", "content": changed_message})
        
        body = {
            'model': 'gpt-4o',
            'messages': messages_opt,
        }

        response = requests.post(url=self.url, headers=self.header, json=body)
        if response.ok:
            reply = json.loads(response.json())["choices"][0]["message"]["content"]
        else:
            reply = "Не удалось связаться с сервером"
        return reply

    def get_dummy_replic(self, messages):
        body = {
            'model': 'gpt-4o',
            'messages': messages,
        }
        response = requests.post(url=self.url, headers=self.header, json=body)
        if response.ok:
            reply = json.loads(response.json())["choices"][0]["message"]["content"]
        else:
            reply = "Не удалось связаться с сервером"
        return reply


    def get_brain_status(self, messages, last_message,  current_scheme):
        changed_message =""
        if current_scheme == 0:
          changed_message = f'''Последняя реплика человека:{last_message}.
            Сейчас ты находишься на первом этапе диалога. Вы общаетесь со студентом и 
            условие перехода на следующий этап - получено формальное согласие студента начать 
            занятие.
            Оцени по последнему сообщению было ли получено это  согласие. В ответе выведи только 
            "да" или "нет" в зависимости от выполнения условия
            '''

        elif current_scheme == 1:
          changed_message = f'''Последняя реплика человека:{last_message}.
            Сейчас ты находишься на втором этапе. Сейчас вы работаете на написанием outline. 
            Проверь по последнему сообщению - является ли оно написанным студентом outline.
            Исключение: если последнее сообщение все-таки является написанным outline, но 
            сильно не соответствует каким-то критериям , то ответ должен быть "нет"
           В ответе выведи только "да" или "нет" в зависимости от выполнения условия
            '''

        elif current_scheme == 2:
          changed_message = f'''Последняя реплика человека:{last_message}.
            Сейчас ты находишься на третьем этапе. Сейчас вы работаете над написанием самого эссе. 
            Проверь по последнему сообщению и истории- написал ли студент эссе полностью, включая заключение?
            Исключение: если последнее сообщение все-таки является полностью написанным эссе, но сильно не 
            соответствует каким-то критериям , то ответ должен быть "нет"
            В ответе выведи только "да" или "нет" в зависимости от выполнения условия
            '''
        else:
           return
        messages_opt = list(messages)
        messages_opt.append({"role": "user", "content": changed_message})
        
        
        body = {
            'model': 'gpt-4o',
            'messages': messages_opt,
        }

        response = requests.post(url=self.url, headers=self.header, json=body)
        if response.ok:
            reply = json.loads(response.json())["choices"][0]["message"]["content"]
        else:
            reply = "Не удалось связаться с сервером"
        return reply

