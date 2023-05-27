from fastapi import HTTPException, status
from .. import models
from ..schemas import User
from sqlalchemy.orm import Session
from ..hashing import Hash


def show(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not found",
        )
    return user


def create_user(user: User, db: Session):
    new_user = models.User(
        name=user.name, email=user.email, password=Hash.bcrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
