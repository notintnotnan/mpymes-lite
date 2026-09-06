from fastapi import FastAPI

from app.core.config import config
from app.db.session import engine
from app.schemas.base import Base

from app.api.v1.business import business_router
from app.api.v1.account import account_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.fastapi_app_name)

app.include_router(business_router, prefix="/api/v1")
app.include_router(account_router, prefix="/api/v1")