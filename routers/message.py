# Routes for sending/fetching messages
from typing import List

from schemas.message import MessageCreate, MessageDisplay
from auth.oauth2 import get_current_user
from fastapi import APIRouter, Depends
from schemas.user import UserDisplay
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_message

router = APIRouter(
    prefix="/message",
    tags=["message"],
)



# Create a new message
@router.post("/", response_model=MessageDisplay)
def create_message(request: MessageCreate, db: Session = Depends(get_db),
                   current_user: UserDisplay = Depends(get_current_user)):
    return db_message.create_message(db, request, buyer_id=current_user.id)


# Read all messages
@router.get("/all")
def get_user_messages(
        db: Session = Depends(get_db),
        current_user: UserDisplay = Depends(get_current_user)
):
    return db_message.get_user_messages(db, current_user.id)



# Delete a message
@router.delete("/delete/{id}")
def delete_message(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    return db_message.delete_message(id, db)
