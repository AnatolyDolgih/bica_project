# сервер для приема и обработки запросов от визуализации 
# сервер должен по полученной реплике сгенерировать ответ 
# виртуального тьютора

from fastapi import FastAPI
import request_contracts as rc
import virtual_tutor as vt

app = FastAPI()
actor = vt.VirualTutor()

@app.get("/")
def process_root():
    return {"message" : "Virtual Tutor project v1.0"}

# Обработка текста и выдача ответа
@app.post("/getAnswer")
def process_post_text(item: rc.TextItem):
    user_replic = item.input
    vt_reply = actor.generate_answer(user_replic)
    return {
            "Desk": "Что-то для доски",
            "Reply": vt_reply,
            "Direction": "Player",
            "Happy": 1,
            "Sad": 0.05,
            "Surprise": 0,
            "Disgust": 0,
            "Angry": 0,
            "Afraid": 0
    }

# Обработка эмоции и выдача результата
@app.post("/getEmotion")
def process_post_emotion(item: rc.EmotionItem):
    pass