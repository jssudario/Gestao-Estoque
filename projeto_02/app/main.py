from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.v1.router import api_router

# cria tabelas (didático; em produção use alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health():
    return {"status": "ok"}