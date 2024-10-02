from fastapi import FastAPI

from src.storage.router import router as storage_router

app = FastAPI()

app.include_router(router=storage_router)
