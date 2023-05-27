from fastapi import APIRouter, Depends, status, HTTPException
from .. import models, token
from ..schemas import Login
from ..database import get_db
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
