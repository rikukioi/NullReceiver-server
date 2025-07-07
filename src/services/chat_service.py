from fastapi import WebSocket


class MessageDeliveryService:
    async def personal_message(
        self,
        receiver_socket: WebSocket,
        message: str,
        sender: str,
    ) -> None:
        try:
            await receiver_socket.send_json(
                {
                    "sender": sender,
                    "message": message,
                }
            )
        except Exception:
            raise ValueError("Получатель оффлайн.")

    async def broadcast_message(
        self,
        receiver_sockets: list[WebSocket],
        message: str,
        sender: str,
    ) -> None:
        for socket in receiver_sockets:
            try:
                await socket.send_json(
                    {
                        "sender": sender,
                        "message": message,
                    }
                )
            except Exception:
                continue
