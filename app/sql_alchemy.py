from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict


from app.database import engine
from app import models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str
    content: str
    published: bool = True
