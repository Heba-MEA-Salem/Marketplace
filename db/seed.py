# Seed for making ads temporarily

from db.database import SessionLocal
from db.models import DbCategory


def seed_categories():
    db = SessionLocal()
    try:
        if db.query(DbCategory).count() == 0:
            db.add_all([
                DbCategory(name="Electronics"),
                DbCategory(name="Furniture"),
                DbCategory(name="Clothing"),
                DbCategory(name="Jewelry"),
                DbCategory(name="Appliances"),
            ])
            db.commit()
    finally:
        db.close()

