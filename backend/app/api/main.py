from fastapi import FastAPI

from app.api.routes import chat, health, jobs, notes
from app.core.settings import get_settings

app = FastAPI(title=f"{get_settings().app_name} API", version="0.1.0")
app.include_router(health.router)
app.include_router(notes.router)
app.include_router(jobs.router)
app.include_router(chat.router)
