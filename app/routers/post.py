from fastapi import status, HTTPException, Depends, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from ..database import get_db

from .. import models, schemas, oauth2
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()

    # results = db.query(models.Post, func.count(models.Vote.post_id).label("count")). \
    #     join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True). \
    #     group_by(models.Post.id).all()

    # print(results)

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def add_post(post: schemas.PostCreate, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,
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

    results = db.query(models.Post.id, func.count(models.Vote.post_id).label("count")).\
        join(models.Vote, models.Vote.post_id == models.Post.id).\
        filter(models.Post.id == id).\
        group_by(models.Post.id).first()

    return post, {"likes": results.count}


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exist")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

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
