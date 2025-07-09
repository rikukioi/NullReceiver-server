import logging
from logging.handlers import RotatingFileHandler

from .app_config import APP_DIR


def ensure_logs_dir_exist() -> None:
    logs_dir = APP_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)


def configure_third_party_loggers(prod: bool = True) -> None:
    if prod:
        logging.getLogger("uvicorn").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

        logging.getLogger("fastapi").setLevel(logging.INFO)
        logging.getLogger("starlette").setLevel(logging.WARNING)

        logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
        logging.getLogger("sqlalchemy.dialects").setLevel(logging.ERROR)

        logging.getLogger("alembic").setLevel(logging.INFO)

        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("asyncpg").setLevel(logging.WARNING)
    else:
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("uvicorn.error").setLevel(logging.INFO)
        logging.getLogger("uvicorn.access").setLevel(logging.INFO)

        logging.getLogger("fastapi").setLevel(logging.DEBUG)
        logging.getLogger("starlette").setLevel(logging.DEBUG)

        logging.getLogger("sqlalchemy").setLevel(logging.INFO)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
        logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)
        logging.getLogger("sqlalchemy.dialects").setLevel(logging.INFO)

        logging.getLogger("alembic").setLevel(logging.DEBUG)

        logging.getLogger("httpx").setLevel(logging.INFO)
        logging.getLogger("asyncpg").setLevel(logging.INFO)


def configure_logging(level=logging.INFO) -> None:
    formatter = logging.Formatter(
        fmt="[%(asctime)s] | %(levelname)7s | [%(module)15s:%(lineno)3d] | %(message)s",
        datefmt="%Y-%m-%d  %H:%M:%S",
    )

    ensure_logs_dir_exist()

    file_handler = RotatingFileHandler(
        filename=APP_DIR / "logs" / "app.log",
        maxBytes=10_000_000,
        encoding="UTF-8",
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    error_handler = RotatingFileHandler(
        filename=APP_DIR / "logs" / "error.log",
        maxBytes=10_000_000,
        encoding="UTF-8",
        backupCount=5,
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(console_handler)
