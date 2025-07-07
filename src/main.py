import uvicorn
from fastapi import FastAPI
from src.routes.auth import router as auth_router
from src.routes.websocket import router as ws_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(ws_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=23156, reload=True, reload_delay=5)
