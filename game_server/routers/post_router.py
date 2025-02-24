from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from game_server.configs import get_db

from game_server.services.post_service import PostService, PostCreate, PostUpdate
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
post_service = PostService()


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime = None
    author_id: int

    class Config:
        orm_mode = True


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, author_id: int, db: Session = Depends(get_db)):
    return post_service.create_post(db=db, post_data=post, author_id=author_id)


@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_post(db=db, post_id=post_id)


@router.get("/", response_model=List[PostResponse])
def read_posts(skip: int = 0, limit: int = 100, published_only: bool = True, db: Session = Depends(get_db)):
    return post_service.get_posts(db=db, skip=skip, limit=limit, published_only=published_only)


@router.get("/user/{user_id}", response_model=List[PostResponse])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return post_service.get_user_posts(db=db, user_id=user_id, skip=skip, limit=limit)


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    return post_service.update_post(db=db, post_id=post_id, post_data=post)


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.delete_post(db=db, post_id=post_id)