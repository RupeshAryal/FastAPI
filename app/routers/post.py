from fastapi import  status, HTTPException, Depends, APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

from .. import models, schemas, oauth2
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def add_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int =  Depends(oauth2.get_current_user)):
    new_post = models.Post(
        **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post_id(id: int, db: Session = Depends(get_db)):
    query_result = db.query(models.Post).filter(models.Post.id == id)

    post = query_result.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist"
                            )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return {"detail": "post deleted"}


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()
    if post1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post1
