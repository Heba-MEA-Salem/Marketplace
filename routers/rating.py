# Routes for rating users and viewing ratings

from fastapi import APIRouter, Depends, status, Query
from schemas.ads import AdCreate, AdPublic, AdUpdate, AdStatusUpdate
from auth.oauth2 import get_current_user
from schemas.rating import RatingCreate, RatingDisplay
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from db import db_rating
from schemas.user import UserDisplay

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.post("/ads/{ad_id}", response_model=RatingDisplay, status_code=status.HTTP_201_CREATED)
def rate_ad(
        ad_id: int,
        payload: RatingCreate,
        db: Session = Depends(get_db),
        CurrentUser: UserDisplay = Depends(get_current_user)
):
    return db_rating.create_rating(db=db, ad_id=ad_id, rater_id=CurrentUser.id, score=payload.score)