# FastAPI app, includes routers, runs server
import uvicorn

from routers import user, ads, category, message, rating
from auth import authentication
from db.database import engine
from fastapi import FastAPI
from db import models, seed

app = FastAPI()
app.include_router(user.router)

app.include_router(ads.router)

app.include_router(category.router)

app.include_router(message.router)

app.include_router(authentication.router)

app.include_router(rating.router)


@app.get("/")
def index():
    return "Hello Team 1"


models.Base.metadata.create_all(engine)

seed.seed_categories()

if __name__ == "__main__":
    # Important: disable reload while debugging
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="debug",
    )
