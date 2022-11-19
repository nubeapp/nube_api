from fastapi import FastAPI

from . import models
from .database import engine, get_db
from .routers import tmpcode, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(tmpcode.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to my API!"}
