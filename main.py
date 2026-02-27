# FastAPI app, includes routers, runs server

from db.database import engine
from fastapi import FastAPI
from routers import user, ads
from db import models

from db.database import SessionLocal
from db.models import Category
from db.models import Advertisement

app = FastAPI()
app.include_router(user.router)

app.include_router(ads.router)


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


@app.get("/")
def index():
    return "Hello Team 1"


models.Base.metadata.create_all(engine)
