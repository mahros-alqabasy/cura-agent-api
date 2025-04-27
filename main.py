from fastapi import FastAPI
from api.v1.api_v1 import api_router
from core.config import settings
from db.session import engine
from db.base_class import Base
from db.models import user

from db.models import User, Role, Permission


from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Hospital Information System - Cura Agent",
    description="Backend API for HIS that supports LLMs and multiple roles",
    version="1.0.0",
)

@app.get("/")
async def root():
    return RedirectResponse(url="https://cura-agent-api-production.up.railway.app/docs")

    
# Create all tables automatically
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)
