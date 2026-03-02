# Routes for sending/fetching messages

from fastapi import APIRouter, Depends, status
from schemas.message import MessageCreate, MessageDisplay
from sqlalchemy.orm import Session
from db import db_message
from db.database import get_db



router = APIRouter(
    prefix="/message",
    tags=["message"],
)

@router.post("/", response_model= MessageDisplay )
def create_message(request: MessageCreate, db: Session = Depends(get_db)):
    return db_message.create_message(db, request)