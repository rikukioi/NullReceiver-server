import logging
from logging.handlers import RotatingFileHandler

from .app_config import APP_DIR


def ensure_logs_dir_exist() -> None:
    logs_dir = APP_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)


def configure_third_party_loggers(level=logging.DEBUG) -> None:
    # Очистка от сторонних хэндлеров
    third_party_loggers = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "sqlalchemy",
        "sqlalchemy.engine",
        "sqlalchemy.pool",
    ]
    for logger_name in third_party_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.handlers.clear()
        logger.propagate = True

    # Отключение логгеров
    loggers_to_disable = [
        "sqlalchemy.orm.mapper",
    ]
    for logger_name in loggers_to_disable:
        logger = logging.getLogger(logger_name)
        logger.disabled = True
        logger.propagate = False


def configure_logging(level=logging.INFO) -> None:
    formatter = logging.Formatter(
        fmt="[%(asctime)s.%(msecs)03d] | %(levelname)7s | [%(name)s] - %(message)s",
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

    configure_third_party_loggers()
