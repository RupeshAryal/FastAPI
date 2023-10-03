from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException

from fastapi.params import Body
from pydantic import BaseModel, ConfigDict
from random import randrange
import mysql.connector

from sqlalchemy.orm import Session
import models
from database import engine, Base, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str
    content: str
    published: bool = True
