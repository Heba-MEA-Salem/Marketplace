from requests import Session
from schemas.user import UserCreate, UserLogin
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from db.models import DbCategory
from typing import Optional



# Get all categories
def get_categories(db: Session):
    return db.query(DbCategory).all()
