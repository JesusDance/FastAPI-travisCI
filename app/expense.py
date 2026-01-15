from typing import List

from sqlmodel import select
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.db import SessionDep
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.security import decode_token


router = APIRouter(prefix="/expenses", tags=["expenses"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/", response_model=ExpenseRead, status_code=201)
def create_expense(expense: ExpenseCreate,
                   session: SessionDep,
                   token: str = Depends(oauth2_scheme)):

    user_id = int(decode_token(token))
    db_expense = Expense(**expense.model_dump(), user_id=user_id)

    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)

    return db_expense


@router.get("/", response_model=List[ExpenseRead])
def get_expenses(session: SessionDep,token: str = Depends(oauth2_scheme)):
    user_id = int(decode_token(token))
    expenses = session.exec(select(Expense).where(Expense.user_id == user_id)).all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int,
                session: SessionDep,
                token: str = Depends(oauth2_scheme)):

    user_id = int(decode_token(token))
    expense = session.get(Expense, expense_id)

    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="You don't have access to this expense")

    return expense


@router.patch("/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: int,
                   expense_update: ExpenseUpdate,
                   session: SessionDep,
                   token: str = Depends(oauth2_scheme)):

    user_id = int(decode_token(token))
    expense = session.get(Expense, expense_id)

    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="You don't have access to this expense")

    update_data = expense_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(expense, key, value)

    session.commit()
    session.refresh(expense)

    return expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: int,
                   session: SessionDep,
                   token: str = Depends(oauth2_scheme)):

    user_id = int(decode_token(token))
    expense = session.get(Expense, expense_id)

    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="You don't have access to this expense")

    session.delete(expense)
    session.commit()

    return {"message": f"Expense {expense_id} deleted successfully"}