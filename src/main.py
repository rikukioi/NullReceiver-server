from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.core.log_config import configure_logging
from src.routes.auth import router as auth_router
from src.routes.websocket import router as ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(level=10)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(ws_router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=23156,
        reload=True,
        reload_delay=5,
        log_config=None,
    )
