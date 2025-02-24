from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from game_server.models.models import Comment, Post, User


class CommentManager:
    def create_comment(self, db: Session, content: str, author_id: int, post_id: int):
        # Check if user exists
        user = db.query(User).filter(User.id == author_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if post exists
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        # Create comment
        db_comment = Comment(content=content, author_id=author_id, post_id=post_id)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def get_comment_by_id(self, db: Session, comment_id: int):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        return comment

    def get_post_comments(self, db: Session, post_id: int, skip: int = 0, limit: int = 100):
        return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()

    def get_user_comments(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return db.query(Comment).filter(Comment.author_id == user_id).offset(skip).limit(limit).all()

    def update_comment(self, db: Session, comment_id: int, content: str):
        comment = self.get_comment_by_id(db, comment_id)
        comment.content = content
        db.commit()
        db.refresh(comment)
        return comment

    def delete_comment(self, db: Session, comment_id: int):
        comment = self.get_comment_by_id(db, comment_id)
        db.delete(comment)
        db.commit()
        return {"message": "Comment deleted successfully"}