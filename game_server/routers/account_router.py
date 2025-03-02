from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from game_server.configs import get_db
from game_server.forms.user_form import UserCreate, UserUpdate
from game_server.schemas.user_schema import UserResponse
from game_server.services.auth_service import AuthService

from game_server.services.user_service import UserService

router = APIRouter()
user_service = UserService()
auth_service = AuthService()


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def login(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.login(db=db, user_data=user)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db=db, user_id=user_id)


@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_users(db=db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db=db, user_id=user_id, user_data=user)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db=db, user_id=user_id)
