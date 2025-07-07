from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    def connect(self, username: str, websocket: WebSocket) -> None:
        self.active_connections[username] = websocket

    def disconnect(self, username: str) -> None:
        self.active_connections.pop(username, None)

    def get_for_broadcast(self) -> list[WebSocket]:
        return list(self.active_connections.values())

    def get_user_sock(self, username: str) -> WebSocket | None:
        return self.active_connections.get(username)
