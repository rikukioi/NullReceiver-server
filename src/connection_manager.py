from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, nickname: str, websocket: WebSocket):
        self.active_connections[nickname] = websocket

    def disconnect(self, nickname: str):
        if nickname in self.active_connections:
            del self.active_connections[nickname]

    async def personal_message(self, message: str, nickname: str, sender: str):
        if nickname in self.active_connections:
            try:
                await self.active_connections[nickname].send_json(
                    {"sender": sender, "message": message}
                )
            except Exception as e:
                print(f"Ошибка отправки сообщения для {nickname}: {e}")
                raise ValueError(f"Client {nickname} is offline")

    async def broadcast(self, message: str, sender: str):
        for nickname, connection in self.active_connections.items():
            try:
                await connection.send_json({"sender": sender, "message": message})
            except Exception as e:
                print(f"Ошибка broadcast для {nickname}: {e}")
