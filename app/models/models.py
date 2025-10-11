from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    balance: float = Field(default=1000.0)

    transactions_sent: List["Transaction"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "Transaction.from_user_id"},
    )
    transactions_received: List["Transaction"] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs={"foreign_keys": "Transaction.to_user_name"},
    )


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_user_id: int = Field(foreign_key="user.id")
    to_user_name: int = Field(foreign_key="user.username")
    amount: float
    description: str

    sender: User = Relationship(
        back_populates="transactions_sent",
        sa_relationship_kwargs={"foreign_keys": "Transaction.from_user_id"},
    )
    receiver: User = Relationship(
        back_populates="transactions_received",
        sa_relationship_kwargs={"foreign_keys": "Transaction.to_user_name"},
    )
