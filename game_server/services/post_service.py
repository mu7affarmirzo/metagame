from sqlalchemy.orm import Session
from game_server.data_managers.post_manager import PostManager
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostUpdate(BaseModel):
    title: str = None
    content: str = None
    published: bool = None


class PostService:
    def __init__(self):
        self.post_manager = PostManager()

    def create_post(self, db: Session, post_data: PostCreate, author_id: int):
        return self.post_manager.create_post(
            db=db,
            title=post_data.title,
            content=post_data.content,
            author_id=author_id,
            published=post_data.published
        )

    def get_post(self, db: Session, post_id: int):
        return self.post_manager.get_post_by_id(db, post_id)

    def get_posts(self, db: Session, skip: int = 0, limit: int = 100, published_only: bool = True):
        return self.post_manager.get_all_posts(db, skip, limit, published_only)

    def get_user_posts(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return self.post_manager.get_user_posts(db, user_id, skip, limit)

    def update_post(self, db: Session, post_id: int, post_data: PostUpdate):
        update_data = post_data.dict(exclude_unset=True)
        return self.post_manager.update_post(db, post_id, update_data)

    def delete_post(self, db: Session, post_id: int):
        return self.post_manager.delete_post(db, post_id)