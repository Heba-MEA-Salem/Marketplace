# Routes for user actions (register, login, update)

from schemas.user import UserDisplay, UserCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


# Create a user (Register)
@router.post("/", response_model=UserDisplay)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# User log in

# User log out

# Read / display / get users  (one user - all)

# Update user

# Delete user