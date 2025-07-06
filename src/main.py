import uvicorn
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect

from src.routes.auth import router as auth_router
from src.services.ws_connection_manager import WSConnectionManager

app = FastAPI()
app.include_router(auth_router)

manager = WSConnectionManager()


@app.websocket("/ws")
async def websocket(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        nickname = await websocket.receive_text()
        await manager.connect(nickname, websocket)

        print(f"Подключился {nickname}")

        while True:
            data = await websocket.receive_json()

            if data["nickname"] == "broadcast":
                await manager.broadcast(data["message"], nickname)
            else:
                try:
                    await manager.personal_message(
                        data["message"], data["nickname"], nickname
                    )
                except ValueError:
                    await websocket.send_text(f"Client {data['nickname']} is offline")

    except WebSocketDisconnect:
        manager.disconnect(nickname)
        print(f"Отключился {nickname}")


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=23156, reload=True, reload_delay=5)
