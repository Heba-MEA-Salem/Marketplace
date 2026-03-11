# Message input/output schemas
from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    ad_id: int
    seller_id: int
    message_body: str



class MessageDisplay(BaseModel):
    id: int
    ad_id: int
    buyer_id: int
    seller_id: int
    message_body: str
    created_at: datetime
    model_config= {"from_attributes": True}