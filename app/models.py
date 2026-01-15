from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str

    expenses: List["Expense"] = Relationship(back_populates="user")


class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    amount: int
    description: str | None = None

    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="expenses")