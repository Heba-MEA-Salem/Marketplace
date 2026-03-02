# CRUD for Ads

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import DbCategory
from db.models import DbAds
from schemas.ads import AdCreate, AdPublic


# create_ads()
def create_ad(
        payload: AdCreate,
        db: Session = Depends(get_db),
):
    category = db.query(DbCategory).filter(DbCategory.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")

    ad = DbAds(
        seller_id=payload.seller_id,
        category_id=payload.category_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
    )
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


# get_ad_by_id()
def get_ad(db: Session, id: int):
    ad = db.query(DbAds).filter(DbAds.id == id).first()

    if not ad:
        raise HTTPException(status_code=404, detail=f"Ad with id {id} is not found")
    return ad



# update_ads()
# delete_ads()
# search_ads_by_category_or_recency()


