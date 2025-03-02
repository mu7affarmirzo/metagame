import random

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from game_server.models.models import Account
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AccountManager:
    def create_user(self, db: Session, username: str):
        account = Account(nickname=username, credits=0.0)
        login_credits = random.uniform(self.min_credits, self.max_credits)
        account.credits += login_credits

        # Create user
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def get_user_by_username(self, db: Session, username: str):
        account = db.query(Account).filter(Account.username == username).first()
        if not account:
            return None
        return account

    def update_user(self, db: Session, username: str, credit: int):
        user = self.get_user_by_username(db, username)
        user.credits += credit
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user_by_id(db, user_id)
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
