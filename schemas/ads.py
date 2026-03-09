# Ads input/output schemas

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from db.models import AdStatus


class AdCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10)
    price: int = Field(gt=0)
    category_id: int


class AdPublic(BaseModel):
    id: int
    title: str
    description: str
    price: int
    category_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=120)
    description: Optional[str] = Field(default=None, min_length=10)
    price: Optional[int] = Field(default=None, gt=0)
    category_id: Optional[int] = None


class AdStatusUpdate(BaseModel):
    status: AdStatus
