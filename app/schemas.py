from sqlmodel import SQLModel
from pydantic import BaseModel, constr



class Token(SQLModel):
    access_token: str
    token_type: str


class ExpenseCreate(SQLModel):
    title: str
    amount: int
    description: str | None = None


class ExpenseRead(SQLModel):
    id: int
    title: str
    amount: int
    description: str | None = None


class ExpenseUpdate(SQLModel):
    title: str | None = None
    amount: int | None = None
    description: str | None = None


class UserCreate(BaseModel):
    username: str
    password: constr(min_length=4)


class UserRead(SQLModel):
    id: int
    username: str
    expenses: list[ExpenseRead]





