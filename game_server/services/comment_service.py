from sqlalchemy.orm import Session
from game_server.data_managers.comment_manager import CommentManager
from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentService:
    def __init__(self):
        self.comment_manager = CommentManager()

    def create_comment(self, db: Session, comment_data: CommentCreate, author_id: int, post_id: int):
        return self.comment_manager.create_comment(
            db=db,
            content=comment_data.content,
            author_id=author_id,
            post_id=post_id
        )

    def get_comment(self, db: Session, comment_id: int):
        return self.comment_manager.get_comment_by_id(db, comment_id)

    def get_post_comments(self, db: Session, post_id: int, skip: int = 0, limit: int = 100):
        return self.comment_manager.get_post_comments(db, post_id, skip, limit)

    def get_user_comments(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return self.comment_manager.get_user_comments(db, user_id, skip, limit)

    def update_comment(self, db: Session, comment_id: int, comment_data: CommentUpdate):
        return self.comment_manager.update_comment(db, comment_id, comment_data.content)

    def delete_comment(self, db: Session, comment_id: int):
        return self.comment_manager.delete_comment(db, comment_id)