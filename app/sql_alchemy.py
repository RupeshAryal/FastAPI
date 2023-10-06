from fastapi import FastAPI
from app.database import engine
from app import models
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)

