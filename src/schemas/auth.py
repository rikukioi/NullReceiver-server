from pydantic import BaseModel


class UserAuthData(BaseModel):
    username: str
    password: str


class UserInDatabase(BaseModel):
    id: int
    username: str
    password: bytes

    model_config = {
        "from_attributes": True,
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
