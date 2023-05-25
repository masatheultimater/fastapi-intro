from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import Blog, ShowBlog, User, ShowUser
from .models import Base
from . import models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash


app = FastAPI()

Base.metadata.create_all(engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog", response_model=List[ShowBlog], tags=["Blog"])
def all_fetch(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(
    "/blog/{id}", status_code=status.HTTP_200_OK, response_model=ShowBlog, tags=["Blog"]
)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Blog with id {id} is not found"}
    return blog


@app.get("/user/{id}", response_model=ShowUser, tags=["user"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"User with id {id} is not found"}
    return user


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create_blog(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.post("/user", status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
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


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blog"])
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found",
        )
    blog.update(request.dict())
    db.commit()

    return "Update completed"
