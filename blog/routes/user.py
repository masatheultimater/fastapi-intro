from fastapi import Depends, APIRouter, HTTPException, status
from .. import models
from ..database import get_db
from ..schemas import User, ShowUser
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/{id}", response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not found",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
