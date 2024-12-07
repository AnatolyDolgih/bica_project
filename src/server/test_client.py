# import requests
# import json

# response = requests.get("https://bica-project.tw1.ru/")
# print(response)

# response_post_1 = requests.post("https://bica-project.tw1.ru/getAnswerDialog",\
#     json.dumps({"input_text" : "I'm post for dialog"}))
# print(response_post_1)

# response_post_2 = requests.post("http://bica-project.tw1.ru/getAnswerEssay/",\
#     json.dumps({"input_text" : "I'm post for essay"}))
# print(response_post_2)


import requests

url = 'https://www.bicaai2023.org/openai/v1/chat/completions'

headers = {
    'Authorization': 'Bearer x_cTiM9n_TLr80E85jjr4fSm4OfTTL8m3GyG_UOvoRLf7ajZDKvpEMgTDsQtacRwjoniI3qfaUKpJ-2lOEFY1g',
}

body = {
    'model': 'gpt-4o',
    'messages': [
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        },
        {
            'role': 'user',
            'content': 'Hello!'
        }
    ]
}

response = requests.post(url=url, headers=headers, json=body)

print(response.json())
