# Ads input/output schemas

from pydantic import BaseModel, Field
from datetime import datetime


class AdCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10)
    price: int = Field(gt=0)
    category_id: int
    seller_id: int


class AdPublic(BaseModel):
    id: int
    title: str
    description: str
    price: int
    category_id: int
    seller_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
