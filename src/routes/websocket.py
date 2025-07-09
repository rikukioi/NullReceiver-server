import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.websockets import WebSocket, WebSocketDisconnect

from src.core.auth_utils import validate_token
from src.services import MessageRouter, SocketManager

router = APIRouter(tags=["WEBSOCKET"])

msg_router = MessageRouter()

logger = logging.getLogger(__name__)


@router.websocket("/ws")
async def websocket(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
) -> None:
    try:
        username = validate_token(token=token)
    except HTTPException:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Невалидный токен.",
        )
        return

    await websocket.accept()
    
    SocketManager.connect(username, websocket)
    logging.info("Подключился %s", username)
    try:
        while True:
            data = await websocket.receive_json()

            await msg_router.route(
                data=data,
                sender_socket=websocket,
            )

    except WebSocketDisconnect:
        SocketManager.disconnect(username)
        logging.info("Отключился %s", username)
