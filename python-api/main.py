from fastapi import FastAPI
from .database import Base, engine
from .routers import tasks, users, categories
from .error_handlers import add_error_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToDo List API", version="1.0.0")

app.include_router(users.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

add_error_handlers(app)
