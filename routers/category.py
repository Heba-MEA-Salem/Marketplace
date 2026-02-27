from schemas.category import CategoryDisplay, CategoryBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_category
from typing import List




router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.post("/new", response_model= CategoryDisplay)
def new_category(request: CategoryBase, db: Session = Depends(get_db)):
    return db_category.add_category(db, request)


@router.get("/all", response_model=List[CategoryDisplay])
def get_categories(db: Session = Depends(get_db)):
    return db_category.get_categories(db)