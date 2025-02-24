from sqlalchemy.orm import Session
from game_server.data_managers.user_manager import UserManager
from game_server.forms.user_form import UserCreate, UserUpdate


class UserService:
    def __init__(self):
        self.user_manager = UserManager()

    def create_user(self, db: Session, user_data: UserCreate):
        return self.user_manager.create_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )

    def get_user(self, db: Session, user_id: int):
        return self.user_manager.get_user_by_id(db, user_id)

    def get_user_by_email(self, db: Session, email: str):
        return self.user_manager.get_user_by_email(db, email)

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return self.user_manager.get_all_users(db, skip, limit)

    def update_user(self, db: Session, user_id: int, user_data: UserUpdate):
        update_data = user_data.dict(exclude_unset=True)
        return self.user_manager.update_user(db, user_id, update_data)

    def delete_user(self, db: Session, user_id: int):
        return self.user_manager.delete_user(db, user_id)
