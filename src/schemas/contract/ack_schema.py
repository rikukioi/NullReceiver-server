from pydantic import BaseModel


class AckSchema(BaseModel):
    message_id: str
    to_username: str
