from fastapi import APIRouter, Depends, HTTPException, status

from src.core.auth_utils import check_password, encode_jwt, hash_password
from src.database import UnitOfWork, get_auto_session
from src.schemas import TokenResponse, UserAuthData

router = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    data: UserAuthData,
    uow: UnitOfWork = Depends(get_auto_session),
):
    usr_exist = await uow.user_repo.username_exists(username=data.username)
    if usr_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким ником уже существует.",
        )

    uow.user_repo.add_in_session(
        username=data.username,
        hashed_pass=hash_password(data.password),
    )
    return {
        "message": "Пользователь успешно зарегистрирован.",
    }


@router.post("/login", response_model=TokenResponse)
async def login_user(
    data: UserAuthData,
    uow: UnitOfWork = Depends(get_auto_session),
):
    usr_in_base = await uow.user_repo.get_user(username=data.username)
    if usr_in_base is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователя с таким ником не существует.",
        )

    if not check_password(data.password, usr_in_base.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введенный пароль не является верным.",
        )

    jwt_payload = {
        "id": usr_in_base.id,
        "username": usr_in_base.username,
    }
    return TokenResponse(
        access_token=encode_jwt(payload=jwt_payload),
        token_type="Bearer",
    )
