import logging
from typing import Any

from fastapi.websockets import WebSocket
from pydantic import ValidationError

from src.schemas.contract import (
    AckSchema,
    MessageSchema,
)

from .schema_utils import make_error_payload
from .ws_connection_manager import SocketManager

logger = logging.getLogger(__name__)


async def handle_message(
    data: dict[str, Any],
    sender_sock: WebSocket,
) -> None:
    payload = data.get("payload", {})

    try:
        schema = MessageSchema(**payload)
    except ValidationError:
        logger.debug("Ошибка валидации payload %s", payload)
        await sender_sock.send_json(
            make_error_payload(
                code="INVALID_PAYLOAD",
                detail="Нарушение контракта общения.",
            )
        )
        return

    receiver_sock = SocketManager.get_user_sock(schema.to_username)
    if receiver_sock is None:
        logger.debug(
            "Не удалось получить сокет для пользователя %s",
            schema.to_username,
        )
        await sender_sock.send_json(
            make_error_payload(
                code="USER_OFFLINE",
                detail="Пользователь не в сети.",
                meta={"username": schema.to_username},
            )
        )
        return

    await receiver_sock.send_json(data)
    logger.debug(
        "Успешно доставлено сообщение пользователю %s от пользователя %s",
        schema.to_username,
        schema.from_username,
    )


async def handle_ack(
    data: dict[str, Any],
    sender_sock: WebSocket,
) -> None:
    payload = data.get("payload", {})

    try:
        schema = AckSchema(**payload)
    except ValidationError:
        logger.debug("Ошибка валидации payload %s", payload)
        await sender_sock.send_json(
            make_error_payload(
                code="INVALID_PAYLOAD",
                detail="Нарушение контракта общения.",
            )
        )
        return

    receiver_sock = SocketManager.get_user_sock(schema.to_username)
    if receiver_sock is None:
        logger.debug(
            "Не удалось получить сокет для пользователя %s",
            schema.to_username,
        )
        await sender_sock.send_json(
            make_error_payload(
                code="USER_OFFLINE",
                detail="Пользователь не в сети.",
                meta={"username": schema.to_username},
            )
        )
        return

    await receiver_sock.send_json(data)
    logger.debug(
        "Успешно возвращен ack пользователю %s по message id = %s",
        schema.to_username,
        schema.message_id,
    )
