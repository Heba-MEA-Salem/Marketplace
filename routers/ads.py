# Routes for ads

from fastapi import APIRouter, Depends, status, Header
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.ads import AdCreate, AdPublic, AdUpdate
from db import db_ads

router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("", response_model=AdPublic, status_code=status.HTTP_201_CREATED)
def create_ad(payload: AdCreate, db: Session = Depends(get_db)):
    return db_ads.create_ad(db=db, payload=payload)


@router.get("/{id}", response_model=AdPublic, status_code=status.HTTP_200_OK)
def read_ad(id: int, db: Session = Depends(get_db)):
    return db_ads.get_ad(db, id)


@router.patch("/{ad_id}", response_model=AdPublic)
def update_ad(
        ad_id: int,
        payload: AdUpdate,
        db: Session = Depends(get_db),
        x_seller_id: int = Header(...),  # client must send this header while we dont have authentication
):
    updated_ad = db_ads.update_ad(db=db, ad_id=ad_id, payload=payload, seller_id=x_seller_id)
    return updated_ad


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ad(
        ad_id: int,
        db: Session = Depends(get_db),
        x_seller_id: int = Header(...),
):
    db_ads.delete_ad(db=db, ad_id=ad_id, seller_id=x_seller_id)
    return None
