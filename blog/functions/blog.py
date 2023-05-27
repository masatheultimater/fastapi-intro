from fastapi import HTTPException, status
from .. import models
from ..schemas import Blog
from sqlalchemy.orm import Session


def get_all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
    return blog


def create_blog(blog: Blog, db: Session, current_user):
    user_id = [d for d in current_user]
    user_id = user_id[0].id
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def update_blog(id: int, request: Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
    blog.update(request.dict())
    db.commit()
    return "Update completed"


def delete_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deletion completed"
