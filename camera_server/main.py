from fastapi import FastAPI, WebSocketDisconnect,Request
from starlette.websockets import WebSocket
from fastapi.templating import Jinja2Templates
import uvicorn
import cv2

app = FastAPI()
templates = Jinja2Templates(directory="static")

camera = cv2.VideoCapture("test.mp4")


@app.get("/")
async def home(req: Request):
    return templates.TemplateResponse("index.html", {"request":req})

@app.websocket("/vidws/")
async def get_stream(ws:WebSocket):
    await ws.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                await ws.send_bytes(buffer.tobytes())
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)