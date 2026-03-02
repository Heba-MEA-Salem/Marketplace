# Routes for ads

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.ads import AdCreate, AdPublic
from db import db_ads

router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("", response_model=AdPublic, status_code=status.HTTP_201_CREATED)
def create_ad(payload: AdCreate, db: Session = Depends(get_db)):
    return db_ads.create_ad(db=db, payload=payload)


@router.get("/{id}", response_model=AdPublic, status_code=status.HTTP_200_OK)
def read_ad(id: int, db: Session = Depends(get_db)):
    return db_ads.get_ad(db, id)