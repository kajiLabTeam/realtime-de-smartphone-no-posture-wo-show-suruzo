# WebSocket接続を管理するクラス
from typing import List
from fastapi import WebSocket


class WSManager:
    """
    WebSocket接続を管理するクラス
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        websocket.close()
        self.active_connections.remove(websocket)

    async def send_text(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.active_connections.remove(connection)
