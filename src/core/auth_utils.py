from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt
from fastapi import HTTPException, status

from src.core.app_config import settings


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
    expire_seconds: int = settings.jwt.access_token_expire_seconds,
) -> str:
    to_encode = payload.copy()

    released_at = datetime.now(UTC)
    expire_at = released_at + timedelta(seconds=expire_seconds)
    to_encode.update(
        expire=expire_at,
        release=released_at,
    )

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


def validate_token(token: str | None) -> str:
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload: dict = decode_jwt(token=token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    username = payload.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return username
