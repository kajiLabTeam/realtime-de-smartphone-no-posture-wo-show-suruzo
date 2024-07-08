import json

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.filter import MadgwickFilter
from src.type import validate_sensor_data
from src.wsManager import WSManager


app = FastAPI()
manager = WSManager()
filter = MadgwickFilter()


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.api_route("/", methods=["GET", "POST"])
async def read_root():
    return HTMLResponse("Hello World!")


@app.post("/api/raw")
async def post_raw_data(req: Request):
    """
    HTTP POST でデータを受け取り、WebSocket で接続しているクライアントにデータを送信する
    """

    data = await req.json()
    sensorData = validate_sensor_data(data)

    if sensorData is None:
        return HTMLResponse("Invalid data")

    # フィルターを適用
    quaternions = filter.update(sensorData)

    response_data = {"quaternions": quaternions}

    # データを WebSocket で接続しているクライアントに送信
    await manager.send_text(json.dumps(response_data))

    return response_data


@app.get("/api/init")
async def post_raw_data():
    """
    HTTP GET で初期化リクエストを受け取り、フィルターの初期化を行う
    """

    filter.init()

    return {"message": "Initialized"}


@app.websocket("/ws/posture")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 接続を受け付けるエンドポイント
    """

    # WebSocket 接続を管理するクラスに登録
    await manager.connect(websocket)

    try:
        while True:
            # メッセージを受信
            data = await websocket.receive_text()
            # 全てのクライアントにメッセージを送信
            await manager.send_text(f"Received: {data}")

    except WebSocketDisconnect:
        # WebSocket 接続が切断された場合は解除
        manager.disconnect(websocket)
