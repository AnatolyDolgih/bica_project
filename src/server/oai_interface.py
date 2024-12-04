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
            'Authorization': self.token,
        }
        self.url = config["auth"]["url"]

    def clear_intetions(self, reply):
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", reply)
        numbers = [float(num) if '.' in num else int(num) for num in numbers]
        return(numbers)

    def get_composition(self, intents_dict, fraze):
        cat_str = ', '.join(intents_dict.values())
        num = len(intents_dict.values())
        string = f'''
                Ты механизм по определению интенций в речи человека, связанных с его поведением в различных социальных ситуациях.
                Твоей основной задачей является определить вероятность содержания каждой интенции из сказанного предложения от 0 до 1.
                В твоем распоряжении только {num} интенсиональностей для угадывания (они перечислены через запятую):
                {cat_str}
                Вероятность - число от 0 до 1, где 0 - интенция не содержится совсем, а 1 - содержится точно
                Используй интенции только из указанного списка! Выведи {num} значений вероятности каждой интенциональности в фразе:  
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
        reply = json.loads(response.json())["choices"][0]["message"]["content"]
        return self.clear_intetions(reply)

    def get_replic(self, last_message, messages, intens_dict, feelings, 
                   prev_scheme, current_scheme):
        cat_str = ', '.join(intens_dict.values())
        num = len(intens_dict.values())
        cat_list = list(intens_dict.values())
        prob_int_list = ', '.join(f'{label}: {value}' for label, value in zip(cat_list, feelings))
        changed_message = f'''Последняя реплика человека:{last_message}.
            Сгенерируй фразу - ответ на последнюю реплику человека, в которой содержались бы речевые интенции со следующей вероятностью: {prob_int_list}.
            Если у интенции вероятность от 0 до 0.25, то она не проявляется в речи человека,
            если вероятность от 0.25 до 0.5, то она практически не проявляется в речи человека,
            если вероятность от 0.5 до 0.75, то она косвенно проявляется в репликах человека (не конкретными словами и фразами, а общим настроением)
            если вероятность от 0.75 до 1, то она интенция заметна в речи человека.
            Фраза должна быть не более 20 слов в длину
            Фраза должна содержать не более одного утвердительного предложения или не более одного вопросительного предложения
            Фраза должна быть адекватным и логичным ответом к последней реплике человека.
            Фраза должна быть уместной в контексте всей истории диалога.
            Фраза не должна содержать никакой информации об этапах диалога
            Выведи только новую реплику
            '''

        if current_scheme-prev_scheme == 1 and current_scheme == 2:
            changed_message = hlp.from1to2 + changed_message
        elif current_scheme-prev_scheme == 1 and current_scheme == 3:
            changed_message = hlp.from2to3 + changed_message

        messages_opt = list(messages)
        messages_opt.append({"role": "user", "content": changed_message})
        
        body = {
            'model': 'gpt-4o',
            'messages': messages_opt,
        }

        response = requests.post(url=self.url, headers=self.header, json=body)
        reply = json.loads(response.json())["choices"][0]["message"]["content"]
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

