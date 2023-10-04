from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, ConfigDict

from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: str
    content: str
    published: bool = True



@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'detail': 'post added successfully'}

@app.get("/posts/{id}")
def get_post_id(id: int, db: Session = Depends(get_db)):
    pass

