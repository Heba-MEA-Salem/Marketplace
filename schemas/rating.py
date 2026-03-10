# Rating input/output schemas

from pydantic import BaseModel, Field
from datetime import datetime

class RatingCreate(BaseModel):
    score: int = Field(..., ge=1, le=5)

class RatingDisplay(BaseModel):
    id: int
    ad_id: int
    rater_id: int
    score: int
    created_at: datetime

    model_config= {"from_attributes": True}