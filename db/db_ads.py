# CRUD for Ads
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import DbCategory, AdStatus
from db.models import DbAds
from schemas.ads import AdCreate, AdPublic, AdUpdate


# create_ads()
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


# get_ad_by_id()
def get_ad(db: Session, id: int):
    ad = db.query(DbAds).filter(DbAds.id == id).first()

    if not ad:
        raise HTTPException(status_code=404, detail=f"Ad with id {id} is not found")
    return ad


# update_ads()
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


# delete_ads()
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


# filter_ads_by_category_or_recency()
def filter_ads(
        db: Session,
        category_id: Optional[int] = None,
        days: Optional[int] = None,
        limit: int = 10,
        offset: int = 0
):
    ads = db.query(DbAds).filter(DbAds.status == AdStatus.ACTIVE)
    if category_id is not None:
        ads = ads.filter(DbAds.category_id == category_id)

    if days is not None:
        cutoff = datetime.utcnow() - timedelta(days=days)
        ads = ads.filter(DbAds.created_at >= cutoff)

    return (
        ads
        .order_by(DbAds.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )