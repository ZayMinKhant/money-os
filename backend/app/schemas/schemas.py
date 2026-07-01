from pydantic import BaseModel
from datetime import datetime


# ── Transaction Schemas ──────────────────────────────────────────────────────

class TransactionBase(BaseModel):
    account_id: str
    amount: float
    description: str
    category: str
    type: str  # "income" or "expense"
    date: datetime


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: float | None = None
    description: str | None = None
    category: str | None = None
    type: str | None = None
    date: datetime | None = None


class TransactionResponse(TransactionBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Account Schemas ─────────────────────────────────────────────────────────

class AccountBase(BaseModel):
    name: str
    type: str = "checking"
    currency: str = "USD"


class AccountCreate(AccountBase):
    balance: float = 0.0


class AccountUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    balance: float | None = None
    currency: str | None = None


class AccountResponse(AccountBase):
    id: str
    user_id: str
    balance: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Budget Schemas ───────────────────────────────────────────────────────────

class BudgetBase(BaseModel):
    category: str
    limit: float
    period: str = "monthly"
    start_date: datetime


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category: str | None = None
    limit: float | None = None
    spent: float | None = None
    period: str | None = None


class BudgetResponse(BudgetBase):
    id: str
    user_id: str
    spent: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Dashboard Stats ──────────────────────────────────────────────────────────

class DashboardStatsResponse(BaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    savings_rate: float
    num_accounts: int
    num_transactions: int
