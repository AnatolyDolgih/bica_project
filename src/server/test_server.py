from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from virtual_tutor import VirtualTutor, DummyVirtualTutor

# убираем кэширование файлов, а то плохо выходит
class StaticFilesWithoutCaching(StaticFiles):
    def is_not_modified(self, *args, **kwargs) -> bool:
        return False
    
class EssayItem(BaseModel):
    message: str

class DialogItem(BaseModel):
    message: str

app = FastAPI()
actor = DummyVirtualTutor()

@app.post("/essay")
def read_essay(item: EssayItem):
    print(f"get: {item.message}")
    user_replic = item.message # реплика пользователя
    actor_replic = actor.generate_answer(user_replic) # генерируем реплику тьютора
    return {"message" : "Hello"}

@app.post("/dialog")
def read_dialog(item: DialogItem):
    user_replic = item.message # реплика пользователя
    actor_replic = actor.generate_answer(user_replic) # генерируем реплику тьютора
    return {"message" : "Рудд"}

app.mount("/", StaticFilesWithoutCaching(directory="../ui", html=True), name="static")
