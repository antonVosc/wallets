from fastapi import FastAPI

from app.api.v1.wallets import router as wallets_router

app = FastAPI(
    title="Wallet API",
    description="REST API for managing user wallets",
    version="1.0.0",
)

app.include_router(wallets_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok"}
