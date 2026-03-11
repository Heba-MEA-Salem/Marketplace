# CRUD for Messages

from db.models import DbMessage, DbAds, DbUser
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status
from schemas.message import MessageCreate
from fastapi.params import Depends
from sqlalchemy import or_


# Create message
def create_message(db: Session, request: MessageCreate, buyer_id: int):
    ad = db.query(DbAds).filter(DbAds.id == request.ad_id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")

    buyer = db.query(DbUser).filter(DbUser.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer not found")

    seller = db.query(DbUser).filter(DbUser.id == request.seller_id).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    existing_message = db.query(DbMessage).filter(DbMessage.ad_id == request.ad_id,
                                                  DbMessage.buyer_id == buyer_id).first()

    if existing_message:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Message already exists")

    message = DbMessage(
        ad_id=request.ad_id,
        buyer_id=buyer_id,
        seller_id=request.seller_id,
        message_body=request.message_body
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


# Get messages for user
def get_user_messages(db: Session, user_id: int):
    messages = (
        db.query(DbMessage)
        .filter(
            or_(
                DbMessage.seller_id == user_id,
                DbMessage.buyer_id == user_id
            )
        )
        .order_by(DbMessage.created_at.desc())
        .all()
    )

    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    return messages



# Delete message
def delete_message(message_id: int, db: Session ):
    message = db.query(DbMessage).filter(DbMessage.id == message_id).first()

    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


    db.delete(message)
    db.commit()

    return "Message is deleted"
