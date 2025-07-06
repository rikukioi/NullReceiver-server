from pydantic import BaseModel


class UserAuthData(BaseModel):
    username: str
    password: str
