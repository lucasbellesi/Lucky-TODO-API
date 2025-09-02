from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import tasks, users, categories
from .core.error_handlers import add_error_handlers

Base.metadata.create_all(bind=engine)


app = FastAPI(title="ToDo List API", version="1.0.0")

# Permitir CORS para el frontend local (ajusta el puerto si es necesario)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(users.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

add_error_handlers(app)
