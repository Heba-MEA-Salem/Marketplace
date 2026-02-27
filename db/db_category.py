
from sqlalchemy.orm.session import Session
from db.models import DbCategory




# Get all categories
def get_categories(db: Session):
    return db.query(DbCategory).all()
