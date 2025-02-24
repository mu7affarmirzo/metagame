from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from game_server.models.models import Post, User


class PostManager:
    def create_post(self, db: Session, title: str, content: str, author_id: int, published: bool = True):
        # Check if user exists
        user = db.query(User).filter(User.id == author_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create post
        db_post = Post(title=title, content=content, author_id=author_id, published=published)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    def get_post_by_id(self, db: Session, post_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return post

    def get_all_posts(self, db: Session, skip: int = 0, limit: int = 100, published_only: bool = True):
        query = db.query(Post)
        if published_only:
            query = query.filter(Post.published == True)
        return query.offset(skip).limit(limit).all()

    def get_user_posts(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Post).filter(Post.author_id == user_id).offset(skip).limit(limit).all()

    def update_post(self, db: Session, post_id: int, update_data: dict):
        post = self.get_post_by_id(db, post_id)

        # Update post fields
        for key, value in update_data.items():
            setattr(post, key, value)

        db.commit()
        db.refresh(post)
        return post

    def delete_post(self, db: Session, post_id: int):
        post = self.get_post_by_id(db, post_id)
        db.delete(post)
        db.commit()
        return {"message": "Post deleted successfully"}