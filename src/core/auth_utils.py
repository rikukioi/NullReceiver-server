import jwt
import bcrypt
from typing import Any

from src.core.config import settings


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> str:
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> Any:
    try:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
        )
        return decoded
    except jwt.PyJWTError:
        return None


def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password=password.encode(),
        salt=bcrypt.gensalt(),
    )


def check_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
