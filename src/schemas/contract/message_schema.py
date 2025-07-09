from pydantic import BaseModel


class MessageSchema(BaseModel):
    from_username: str
    to_username: str
    message: str
    message_id: str
