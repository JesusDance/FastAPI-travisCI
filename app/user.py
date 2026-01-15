from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db import SessionDep
from app.models import User
from app.schemas import UserCreate, UserRead, Token
from app.security import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/users", tags=["users"])

#При створенні CRUD-функцій ми завжди додаємо анотовану session.
# Для кожного HTTP-запиту FastAPI створює новий Session-обʼєкт,
# який відкривається і гарантовано закривається завдяки with і yield.
# (створюється не нове TCP-зʼєднання, а новий Session-обʼєкт)

@router.post("/", response_model=UserRead)
def register(user: UserCreate, session: SessionDep):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(username=user.username, password=hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token)
def login(user: UserCreate, session: SessionDep):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(db_user.id)
    return {"access_token": token, "token_type": "bearer"}







