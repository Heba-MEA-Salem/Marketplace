
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from db.database import Base
from sqlalchemy import Column, Enum as SAEnum, text
from sqlalchemy.sql.sqltypes import Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
import enum


# Create the user model
class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    ads = relationship("DbAds", back_populates="seller")


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
