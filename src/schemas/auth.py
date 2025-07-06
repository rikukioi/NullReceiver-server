from pydantic import BaseModel


class UserAuthData(BaseModel):
    username: str
    password: str


class UserInDatabase(BaseModel):
    id: int
    username: str
    hashed_pass: bytes

    model_config = {
        "from_attributes": True,
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
