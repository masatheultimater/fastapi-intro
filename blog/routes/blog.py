from typing import List
from fastapi import FastAPI, APIRouter, Depends, status, HTTPException, Response
from ..schemas import Blog, ShowBlog
from ..database import get_db
from .. import models
from sqlalchemy.orm import Session
from .. functions import blog

router = APIRouter(prefix='/blog', tags=["Blogs"])


@router.get("/", response_model=List[ShowBlog])
def all_fetch(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db)


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blog.get_blog(id, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    return blog.create_blog(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    return blog.delete_blog(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    return blog.update_blog(id, request, db)
