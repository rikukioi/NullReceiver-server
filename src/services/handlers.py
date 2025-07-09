from typing import Any

from fastapi.websockets import WebSocket
from pydantic import ValidationError

from src.schemas.contract import (
    AckSchema,
    MessageSchema,
)

from .schema_utils import make_error_payload
from .ws_connection_manager import SocketManager


async def handle_message(
    data: dict[str, Any],
    sender_sock: WebSocket,
) -> None:
    payload = data.get("payload", {})

    try:
        schema = MessageSchema(**payload)
    except ValidationError:
        sender_sock.send_json(
            make_error_payload(
                code="INVALID_PAYLOAD",
                detail="Нарушение контракта общения.",
            )
        )
        return

    receiver_sock = SocketManager.get_user_sock(schema.to_username)
    if receiver_sock is None:
        await sender_sock.send_json(
            make_error_payload(
                code="USER_OFFLINE",
                detail="Пользователь не в сети.",
                meta={"username": schema.to_username},
            )
        )

    await receiver_sock.send_json(data)


async def handle_ack(
    data: dict[str, Any],
    sender_sock: WebSocket,
) -> None:
    payload = data.get("payload", {})

    try:
        schema = AckSchema(**payload)
    except ValidationError:
        sender_sock.send_json(
            make_error_payload(
                code="INVALID_PAYLOAD",
                detail="Нарушение контракта общения.",
            )
        )
        return

    receiver_sock = SocketManager.get_user_sock(schema.to_username)
    if receiver_sock is None:
        await sender_sock.send_json(
            make_error_payload(
                code="USER_OFFLINE",
                detail="Пользователь не в сети.",
                meta={"username": schema.to_username},
            )
        )

    await receiver_sock.send_json(data)
