from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__file__).parent.parent
PROJECT_DIR = APP_DIR.parent


class DatabaseSettings(BaseModel):
    db: str
    user: str
    password: str
    host: str
    port: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class AuthJWT(BaseModel):
    algorithm: str = "RS256"
    access_token_expire_seconds: int = 600

    private_key_path: Path = APP_DIR / "certs" / "jwt_private.pem"
    public_key_path: Path = APP_DIR / "certs" / "jwt_public.pem"


class Settings(BaseSettings):
    jwt: AuthJWT = AuthJWT()
    postgres: DatabaseSettings

    model_config = SettingsConfigDict(
        env_file=PROJECT_DIR / ".env",
        env_nested_delimiter="_",
        extra="ignore",
    )


settings = Settings()
