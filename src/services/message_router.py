from typing import Any

from fastapi.websockets import WebSocket

from .dispatcher import Dispatcher
from .handlers import (
    handle_ack,
    handle_message,
)
from .schema_utils import make_error_payload


class MessageRouter:
    def __init__(self):
        self._dispatcher = Dispatcher()
        self._dispatcher.register_handler("message", handle_message)
        self._dispatcher.register_handler("ack", handle_ack)

    async def route(
        self,
        data: dict[str, Any],
        sender_socket: WebSocket,
    ) -> None:
        # Проверка типа
        msg_type = data.get("type")
        if not msg_type:
            await sender_socket.send_json(
                make_error_payload(
                    code="NO_TYPE",
                    detail="Неизвестный тип сообщения.",
                )
            )

        # Вызов хэндлера
        handler = self._dispatcher.get_handler(msg_type)
        if not handler:
            await sender_socket.send_json(
                make_error_payload(
                    code="UNKNOWN_TYPE",
                    detail="Тип определяемого сообщения не зарегистрирован в контракте.",
                )
            )

        await handler(data, sender_socket)
