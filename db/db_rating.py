# CRUD for Ratings

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.models import DbUser, DbRating, DbAds
from schemas.rating import RatingCreate, RatingDisplay

# Add a rating
def create_rating(db: Session, ad_id: int, rater_id: int, score:int):
    ad = db.query(DbAds).filter(DbAds.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="Add not found")

    if ad.status != "SOLD":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only sold ads can be rated")

    if ad.buyer_id != rater_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the buyer can rate")

    existing_rating = db.query(DbRating).filter(DbRating.ad_id == ad_id, DbRating.rater_id == rater_id).first()

    if existing_rating:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Rating already exists")

    rating = DbRating(ad_id=ad_id, rater_id=rater_id, score=score)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating



# Get an average rating
# Get ratings for user