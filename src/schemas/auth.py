from pydantic import BaseModel


class UserAuthData(BaseModel):
    nickname: str
    password: str
