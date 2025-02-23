from fastapi import FastAPI

from tau.api import router

app = FastAPI(
    title="Tau Agent API",
    description="API for interacting with Tau agents",
    version="0.1.0",
)

app.include_router(router, prefix="/api")
