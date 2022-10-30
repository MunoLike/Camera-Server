from cgitb import html
from fastapi import FastAPI, WebSocket,WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import uvicorn
import cv2

app = FastAPI()
app.mount("/", StaticFiles(directory="./", html=True), name="static")

camera = cv2.VideoCapture("test.mp4")

@app.websocket("/vidws/")
async def get_stream(ws:WebSocket):
    await ws.accept()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)