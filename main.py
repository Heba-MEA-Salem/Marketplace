# FastAPI app, includes routers, runs server

from routers import user, ads, category, message
from db.database import engine
from fastapi import FastAPI
from db import models, seed


app = FastAPI()
app.include_router(user.router)

app.include_router(ads.router)

app.include_router(category.router)

app.include_router(message.router)


@app.get("/")
def index():
    return "Hello Team 1"


models.Base.metadata.create_all(engine)

seed.seed_categories()