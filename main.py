# FastAPI app, includes routers, runs server

from db.database import engine
from fastapi import FastAPI
from routers import user
from db import models

app = FastAPI()
app.include_router(user.router)



@app.get("/")
def index ():
    return "Hello Team 1"


models.Base.metadata.create_all(engine)