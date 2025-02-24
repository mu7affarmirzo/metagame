from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from game_server.configs import get_db

from game_server.services.comment_service import CommentService, CommentCreate, CommentUpdate
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
comment_service = CommentService()


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime = None
    author_id: int
    post_id: int

    class Config:
        orm_mode = True


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, author_id: int, post_id: int, db: Session = Depends(get_db)):
    return comment_service.create_comment(
        db=db,
        comment_data=comment,
        author_id=author_id,
        post_id=post_id
    )


@router.get("/{comment_id}", response_model=CommentResponse)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comment(db=db, comment_id=comment_id)


@router.get("/post/{post_id}", response_model=List[CommentResponse])
def read_post_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return comment_service.get_post_comments(db=db, post_id=post_id, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[CommentResponse])
def read_user_comments(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return comment_service.get_user_comments(db=db, user_id=user_id, skip=skip, limit=limit)


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)):
    return comment_service.update_comment(db=db, comment_id=comment_id, comment_data=comment)


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.delete_comment(db=db, comment_id=comment_id)