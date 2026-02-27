# Seed for making ads temporarily

from db.database import SessionLocal
from db.models import Category


def seed_categories():
    db = SessionLocal()
    try:
        if db.query(Category).count() == 0:
            db.add_all([
                Category(name="Electronics"),
                Category(name="Furniture"),
                Category(name="Clothing"),
            ])
            db.commit()
    finally:
        db.close()


seed_categories()
