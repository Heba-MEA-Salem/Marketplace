# CRUD for Ads
from fastapi import HTTPException, status
from schemas.ads import AdCreate, AdUpdate
from db.models import DbCategory, AdStatus
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.models import DbAds
from typing import Optional


# Create ads
def create_ad(
        payload: AdCreate,
        db: Session ,
        seller_id: int
):
    category = db.query(DbCategory).filter(DbCategory.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")

    ad = DbAds(
        seller_id=seller_id,
        category_id=payload.category_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
    )
    db.add(ad)
    db.commit()
    db.refresh(ad)
    return ad


# Get ad by id
def get_ad(db: Session, id: int):
    ad = db.query(DbAds).filter(DbAds.id == id).first()

    if not ad:
        raise HTTPException(status_code=404, detail=f"Ad with id {id} is not found")
    return ad


# Update ads
def update_ad(db: Session, ad_id: int, payload: AdUpdate, seller_id: int) -> type[DbAds]:
    ad = db.query(DbAds).filter(DbAds.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    if ad.seller_id != seller_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this advertisement")

    if payload.category_id is not None:
        category = db.query(DbCategory).filter(DbCategory.id == payload.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category_id")
        ad.category_id = payload.category_id

    if payload.title is not None:
        ad.title = payload.title
    if payload.description is not None:
        ad.description = payload.description
    if payload.price is not None:
        ad.price = payload.price

    db.commit()
    db.refresh(ad)
    return ad


# Delete ads
def delete_ad(db: Session, ad_id: int, seller_id: int) -> None:
    ad = db.query(DbAds).filter(DbAds.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    if ad.seller_id != seller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this advertisement"
        )

    db.delete(ad)
    db.commit()


# Filter ads by category or recency
def filter_ads(
        db: Session,
        q: Optional[str] = None,
        category_id: Optional[int] = None,
        days: Optional[int] = None,
        limit: int = 10,
        offset: int = 0
):
    ads = db.query(DbAds).filter(DbAds.status == AdStatus.ACTIVE)
    if q:
        ads = ads.filter((DbAds.title.ilike(f"%{q}%")) | (DbAds.description.ilike(f"%{q}%")))

    if category_id is not None:
        ads = ads.filter(DbAds.category_id == category_id)

    if days is not None:
        cutoff = datetime.utcnow() - timedelta(days=days)
        ads = ads.filter(DbAds.created_at >= cutoff)


    ads = ads.order_by(DbAds.created_at.desc()).offset(offset).limit(limit).all()

    if not ads:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ads found matching your search/filter criteria")

    return ads


# Seller can mark items reserved/sold
def update_ad_status(db: Session, ad_id: int, new_status: AdStatus, seller_id: int):
    ad = db.query(DbAds).filter(DbAds.id == ad_id).first()
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Advertisement not found'
        )

    if ad.seller_id != seller_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this advertisement"
        )

    current_status = ad.status

    valid_changes = {
        AdStatus.ACTIVE: [AdStatus.RESERVED, AdStatus.SOLD],
        AdStatus.RESERVED: [AdStatus.ACTIVE, AdStatus.SOLD],
        AdStatus.SOLD: []
    }

    if new_status not in valid_changes[current_status]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change status from {current_status} to {new_status}"
        )

    ad.status = new_status
    db.commit()
    db.refresh(ad)

    return ad




