from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from game_server.models.models import User
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    def create_user(self, db: Session, username: str, email: str, password: str):
        # Check if user already exists
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = pwd_context.hash(password)

        # Create user
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_id(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_all_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def update_user(self, db: Session, user_id: int, update_data: dict):
        user = self.get_user_by_id(db, user_id)

        # Update user fields
        for key, value in update_data.items():
            if key == "password":
                setattr(user, "hashed_password", pwd_context.hash(value))
            else:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
