from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.hash import Hash
from auth import oauth2
from db import models

router = APIRouter(
  tags=['authentication']
)


@router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InVALID CREDENTIALS")

    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")


    access_token = oauth2.create_access_token(data={'sub': user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }
