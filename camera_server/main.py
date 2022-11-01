from fastapi import FastAPI, WebSocketDisconnect,Request
from starlette.websockets import WebSocket
from fastapi.templating import Jinja2Templates
import uvicorn
import cv2

app = FastAPI()
templates = Jinja2Templates(directory="static")

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
camera.set(cv2.CAP_PROP_CONVERT_RGB, 0.0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print((int(camera.get(cv2.CAP_PROP_FOURCC)).to_bytes(4, 'little').decode('utf-8')))


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
                # ret, buffer = cv2.imencode('.jpg', frame)
                await ws.send_bytes(frame.tobytes())
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    cv2.imwrite()