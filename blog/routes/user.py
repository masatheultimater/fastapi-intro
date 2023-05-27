from fastapi import Depends, APIRouter, HTTPException, status
from .. import models
from ..database import get_db
from ..schemas import User, ShowUser
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..functions import user

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)):

    return user.create_user(request, db)
