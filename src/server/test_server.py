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
    user_replic = item.message # реплика пользователя
    actor.logger_essay.info(user_replic)
    actor_replic = "<Actor reply>"#actor.generate_answer(user_replic) # генерируем реплику тьютора
    return {"message" : actor_replic}

@app.post("/dialog")
def read_dialog(item: DialogItem):
    user_replic = item.message # реплика пользователя
    actor.logger_dialog.info(f"User: {user_replic}")
    actor_replic = "<Actor reply>"#actor.generate_answer(user_replic) # генерируем реплику тьютора
    actor.logger_dialog.info(f"Virtual tutor: {actor_replic}")
    return {"message" : actor_replic}

app.mount("/", StaticFilesWithoutCaching(directory="../ui", html=True), name="static")
