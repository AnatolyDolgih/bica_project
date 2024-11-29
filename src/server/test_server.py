from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
from pydantic.tools import parse_obj_as
from virtual_tutor import VirtualTutor, DummyVirtualTutor
import uvicorn

# убираем кэширование файлов, а то плохо выходит
class StaticFilesWithoutCaching(StaticFiles):
    def is_not_modified(self, *args, **kwargs) -> bool:
        return False

class WssItem(BaseModel):
    type: str
    content: str
    timestamp: str

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

manager = ConnectionManager()

@app.websocket("/test/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        virtual_tutor = DummyVirtualTutor(client_id)
        while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data) 
            data_model = parse_obj_as(WssItem, data_dict)
            actor_replic = virtual_tutor.generate_answer(data_model.content)
            
            if data_model.type == 'chat':
                virtual_tutor.logger_dialog.info(f"User: {data_model.content}")
                virtual_tutor.logger_dialog.info(f"Tutor: {actor_replic}")

            if data_model.type == 'essay':
                virtual_tutor.logger_essay.info(data_model.content)
            
            data_model.content = actor_replic 
            await manager.send_personal_message(data_model.model_dump(), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

app.mount("/test", StaticFilesWithoutCaching(directory="../ui", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
