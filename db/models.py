
from sqlalchemy.sql.sqltypes import Integer, String, Text, DateTime
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy import Column, Enum as SAEnum, text
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import relationship
from db.database import Base
import enum


# Create the user model
class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    ads = relationship("DbAds", back_populates="seller")
    buyer_messages = relationship(
        "DbMessage",
        foreign_keys="DbMessage.buyer_id",
        back_populates="buyer"
    )
    seller_messages = relationship(
        "DbMessage",
        foreign_keys="DbMessage.seller_id",
        back_populates="seller"
    )



# Create the category model
class DbCategory(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    ads = relationship("DbAds", back_populates="category")


# Create the ads model
class AdStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"


class DbAds(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True, index=True)

    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)

    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)  # keep simple for learning

    status = Column(
        SAEnum(AdStatus, name="ad_status"),
        nullable=False,
        server_default=text("'ACTIVE'"),
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    seller = relationship("DbUser", back_populates="ads")
    category = relationship("DbCategory", back_populates="ads")
    messages = relationship("DbMessage", back_populates="ads")



# Create the message model
class DbMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_body = Column(Text, nullable=False)

    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    # one conversation per buyer per ad
    __table_args__ = (
        UniqueConstraint("ad_id", "buyer_id", name="unique_ad_buyer_message"),
    )

    ads = relationship("DbAds", back_populates="messages")
    buyer = relationship("DbUser", foreign_keys=[buyer_id], back_populates="buyer_messages")
    seller = relationship("DbUser", foreign_keys=[seller_id], back_populates="seller_messages")