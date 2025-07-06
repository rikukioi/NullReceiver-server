from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path

APP_DIR = Path(__file__).parent.parent
PROJECT_DIR = APP_DIR.parent


class AuthJWT(BaseModel):
    algorithm: str = "RS256"
    access_token_expire_seconds: int = 600

    private_key_path: Path = APP_DIR / "certs" / "jwt_private.pem"
    public_key_path: Path = APP_DIR / "certs" / "jwt_public.pem"


class Settings(BaseSettings):
    jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(
        env_file=APP_DIR / ".env",
        env_nested_delimiter="__",
    )


settings = Settings()
