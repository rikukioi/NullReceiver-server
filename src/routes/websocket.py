from fastapi import APIRouter, HTTPException, status, Query
from fastapi.websockets import WebSocket, WebSocketDisconnect
from src.core.auth_utils import decode_jwt
from typing import Annotated
from src.services import WSConnectionManager, MessageDeliveryService

router = APIRouter(tags=["WEBSOCKET"])

manager = WSConnectionManager()
message_service = MessageDeliveryService()


@router.websocket("/ws")
async def websocket(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
) -> None:
    if token is None:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Отсутствие токена.",
        )
        return

    try:
        payload: dict = decode_jwt(token=token)
        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен невалиден.",
            )
    except Exception:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Токен невалиден.",
        )
        return

    await websocket.accept()
    manager.connect(username, websocket)
    print(f"Подключился {username}")
    try:
        while True:
            data = await websocket.receive_json()

            if data["username"] == "broadcast":
                sockets = manager.get_for_broadcast()
                await message_service.broadcast_message(
                    sockets,
                    message=data["message"],
                    sender=username,
                )
            else:
                socket = manager.get_user_sock(data["username"])
                if socket is None:
                    await websocket.send_text("Пользователь оффлайн.")
                    continue

                await message_service.personal_message(
                    receiver_socket=socket,
                    message=data["message"],
                    sender=username,
                )

    except WebSocketDisconnect:
        manager.disconnect(username)
        print(f"Отключился {username}")
