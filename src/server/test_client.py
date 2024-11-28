import requests
import json

response = requests.get("https://bica-project.tw1.ru/")
print(response)

response_post_1 = requests.post("https://bica-project.tw1.ru/getAnswerDialog",\
    json.dumps({"input_text" : "I'm post for dialog"}))
print(response_post_1)

response_post_2 = requests.post("http://bica-project.tw1.ru/getAnswerEssay/",\
    json.dumps({"input_text" : "I'm post for essay"}))
print(response_post_2)