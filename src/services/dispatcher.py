from typing import (
    Any,
    Awaitable,
    Callable,
)

from fastapi.websockets import WebSocket

HandlerType = Callable[[dict[str, Any], WebSocket], Awaitable[None]]


class Dispatcher:
    def __init__(self) -> None:
        self.handlers: dict[str, HandlerType] = {}

    def register_handler(
        self,
        message_type: str,
        handler: HandlerType,
    ) -> None:
        self.handlers[message_type] = handler

    def get_handler(
        self,
        message_type: str,
    ) -> HandlerType | None:
        return self.handlers.get(message_type, None)
