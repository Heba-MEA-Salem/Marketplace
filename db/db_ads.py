# CRUD for Advertisement
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Category
from db.models import Advertisement
from schemas.ads import AdCreate, AdPublic


# create_advertisement()
def create_ad(
        payload: AdCreate,
        db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")

    ad = Advertisement(
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
# update_advertisement()
# delete_advertisement()
# search_ads_by_category_or_recency()


