# All tables (or modules: User, Advertisement, Message, Rating)

from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String


# Create the user model
class DbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
