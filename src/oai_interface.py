import numpy as np
import re
import math
import requests
import json
import helper as hlp


class Interface:
    def __init__(self):
        self.token = ""
        with open("./autorization.txt") as file:
            self.token = file.readline()
        self.header = {
            'Authorization': self.token,
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
        #print(response.text)
        reply = json.loads(response.json())["choices"][0]["message"]["content"]
        return self.clear_intetions(reply)
    


if __name__ == "__main__":
    inter = Interface()
    result = inter.get_composition(hlp.ms_1_greetings, "Добрый день, не могли бы вы помочь мне?")
    print(result)