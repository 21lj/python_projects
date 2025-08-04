# launches fastAPI & includes routers

from fastapi import FastAPI
from app.routes import users
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API")

app.include_router(users.router)

