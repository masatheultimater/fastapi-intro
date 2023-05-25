from typing import List
from fastapi import FastAPI, APIRouter, Depends, status, HTTPException, Response
from ..schemas import Blog, ShowBlog
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/blog", response_model=List[ShowBlog], tags=["Blogs"])
def all_fetch(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@router.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBlog,
    tags=["Blogs"],
)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
    return blog


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_blog(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
    blog.delete(synchronize_session=False)
    db.commit()

    return "Deletion completed"


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
    blog.update(request.dict())
    db.commit()

    return "Update completed"