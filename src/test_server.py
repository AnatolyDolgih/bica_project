from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class EssayItem(BaseModel):
    essay: str

class DialogItem(BaseModel):
    message: str

app = FastAPI()

@app.post("/essay")
def read_essay(item: EssayItem):
    print(f"post req {item.essay}")

@app.post("/dialog")
def read_essay(item: DialogItem):
    print(f"post req {item.message}")
    return {"message" : "Hello"}

app.mount("/", StaticFiles(directory="ui", html=True), name="static")
