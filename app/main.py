from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.security import OAuth2PasswordBearer

from app.db import engine
from app.user import router as user_router
from app.expense import router as expense_router


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(expense_router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@app.get("/")
def get_root():
    return {"message": "Welcome to FastAPI!"}
