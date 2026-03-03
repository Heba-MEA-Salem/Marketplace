# Routes for ads
from typing import List, Optional

from fastapi import APIRouter, Depends, status, Header, Query
from schemas.ads import AdCreate, AdPublic, AdUpdate
from auth.oauth2 import oauth2_scheme
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_ads

router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("", response_model=AdPublic, status_code=status.HTTP_201_CREATED)
def create_ad(payload: AdCreate, db: Session = Depends(get_db)):
    return db_ads.create_ad(db=db, payload=payload)

@router.get('/filtered', response_model=List[AdPublic])
def get_filtered_ads(
        category_id: Optional[int] = None,
        days: Optional[int] = None,
        limit: int = Query(10, le=100),
        offset: int = 0,
        db: Session = Depends(get_db)
):
    filtered_ads = db_ads.filter_ads(db=db, category_id=category_id, days=days, limit=limit, offset=offset)
    return filtered_ads

@router.get("/{id}", response_model=AdPublic, status_code=status.HTTP_200_OK)
def read_ad(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db_ads.get_ad(db, id)


@router.patch("/{ad_id}", response_model=AdPublic)
def update_ad(
        ad_id: int,
        payload: AdUpdate,
        db: Session = Depends(get_db),
        x_seller_id: int = Header(...),  # client must send this header while we don't have authentication
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
