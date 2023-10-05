from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, ConfigDict

from sqlalchemy import select
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
    query_result = db.query(models.Post).filter(models.Post.id == id)

    post = query_result.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist"
                            )
    return {'posts': post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    post.delete(synchronize_session = False)
    db.commit()

    return {"detail": "post deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()
    if post1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return {"data": "successful"}




