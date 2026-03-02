# CRUD for Messages

from db.models import DbMessage, DbAds, DbUser
from schemas.message import MessageCreate
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status


# Create_message()
def create_message(db: Session, request:MessageCreate):

    ad = db.query(DbAds).filter(DbAds.id == request.ad_id).first()
    if not ad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ad not found")

    buyer = db.query(DbUser).filter(DbUser.id == request.buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Buyer not found")

    seller = db.query(DbUser).filter(DbUser.id == request.seller_id).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")

    existing_message = db.query(DbMessage).filter(DbMessage.ad_id == request.ad_id, DbMessage.buyer_id == request.buyer_id).first()

    if existing_message:
       raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Message already exists")

    message = DbMessage(
        ad_id = request.ad_id,
        buyer_id = request.buyer_id,
        seller_id = request.seller_id,
        message_body = request.message_body
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message





# get_messages_for_user()
# delete_message()