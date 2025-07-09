import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.websockets import WebSocket, WebSocketDisconnect

from src.core.auth_utils import decode_jwt
from src.services import MessageDeliveryService, WSConnectionManager

router = APIRouter(tags=["WEBSOCKET"])

manager = WSConnectionManager()
message_service = MessageDeliveryService()


logger = logging.getLogger(__name__)


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
    logging.info("Подключился %s", username)
    try:
        while True:
            data = await websocket.receive_json()

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
        logging.info("Отключился %s", username)
