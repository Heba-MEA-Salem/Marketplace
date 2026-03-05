# Routes for ads

from fastapi import APIRouter, Depends, status, Header, Query
from schemas.ads import AdCreate, AdPublic, AdUpdate
from auth.oauth2 import  get_current_user
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from schemas.user import UserDisplay
from db import db_ads


router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("", response_model=AdPublic, status_code=status.HTTP_201_CREATED)
def create_ad(payload: AdCreate, db: Session = Depends(get_db), current_user: UserDisplay=Depends(get_current_user)):
    return db_ads.create_ad(db=db, payload=payload, seller_id=current_user.id)



@router.get('/filtered', response_model=List[AdPublic])
def get_filtered_ads(
        category_id: Optional[int] = None,
        days: Optional[int] = None,
        limit: int = Query(10, le=100),
        offset: int = 0,
        db: Session = Depends(get_db),
        current_user: UserDisplay=Depends(get_current_user)
):
    filtered_ads = db_ads.filter_ads(db=db, category_id=category_id, days=days, limit=limit, offset=offset)
    return filtered_ads



@router.get("/{id}", status_code=status.HTTP_200_OK)
def read_ad(id: int, db: Session = Depends(get_db), current_user: UserDisplay=Depends(get_current_user)):
    return {
        "data": db_ads.get_ad(db=db, id=id),
        "current_user": current_user
    }


@router.patch("/{ad_id}", response_model=AdPublic)
def update_ad(
        ad_id: int,
        payload: AdUpdate,
        db: Session = Depends(get_db),
        x_seller_id: int = Header(...),  # client must send this header while we don't have authentication
        current_user: UserDisplay=Depends(get_current_user)
):
    updated_ad = db_ads.update_ad(db=db, ad_id=ad_id, payload=payload, seller_id=x_seller_id)
    return updated_ad



@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ad(
        ad_id: int,
        db: Session = Depends(get_db),
        x_seller_id: int = Header(...),
        current_user: UserDisplay=Depends(get_current_user)
):
    db_ads.delete_ad(db=db, ad_id=ad_id, seller_id=x_seller_id)
    return None
