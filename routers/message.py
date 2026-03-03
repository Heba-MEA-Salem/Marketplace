# Routes for sending/fetching messages

from schemas.message import MessageCreate, MessageDisplay
from fastapi import APIRouter, Depends, status
from auth.oauth2 import get_current_user
from schemas.user import UserDisplay
from sqlalchemy.orm import Session
from db import db_message
from db.database import get_db

router = APIRouter(
    prefix="/message",
    tags=["message"],
)

@router.post("/", response_model= MessageDisplay )
def create_message(request: MessageCreate, db: Session = Depends(get_db), current_user: UserDisplay=Depends(get_current_user)):
    return db_message.create_message(db, request)