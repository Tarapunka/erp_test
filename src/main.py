from fastapi import FastAPI
from .features.users import router as user_router
from src.features.tasks.routes import router as task_router
from src.features.projects.routes import router as project_router

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
app.include_router(project_router)
