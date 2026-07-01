from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Float, DateTime, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(255), primary_key=True, default=lambda: str(uuid4())
    )
    clerk_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    accounts: Mapped[list["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    budgets: Mapped[list["Budget"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(
        String(255), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(
        String(50), default="checking"
    )  # checking, savings, credit, cash, investment
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), default="USD")

    user: Mapped["User"] = relationship(back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        String(255), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    account_id: Mapped[str] = mapped_column(String(255), index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(10))  # income or expense
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="transactions")
    account: Mapped["Account"] = relationship(back_populates="transactions")


class Budget(Base, TimestampMixin):
    __tablename__ = "budgets"

    id: Mapped[str] = mapped_column(
        String(255), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(100))
    limit: Mapped[float] = mapped_column(Float, nullable=False)
    spent: Mapped[float] = mapped_column(Float, default=0.0)
    period: Mapped[str] = mapped_column(
        String(50), default="monthly"
    )  # monthly, weekly, yearly
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="budgets")
