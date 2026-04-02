import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Ensure create_tables is an async function in app/db/config.py
from app.db.config import create_tables
from app.account.routers import router as account_router
from app.converter.routers import router as converter_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application's lifespan events asynchronously.
    """
    # Startup: Create database tables
    # You MUST await this because it involves async DB I/O
    await create_tables()

    yield

    # Shutdown: Add cleanup logic here if needed
    # e.g., await engine.dispose()

app = FastAPI(lifespan=lifespan)

# Include your routers
app.include_router(account_router, prefix="/api/account", tags=["Account"])
app.include_router(converter_router, prefix="/api/converter", tags=["Converter"])
