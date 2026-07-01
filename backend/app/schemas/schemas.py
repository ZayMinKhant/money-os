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


# ── Financial Profile Schemas ──────────────────────────────────────────────

class FinancialProfileCreate(BaseModel):
    currency: str = "THB"
    salary_day: int = 1


class FinancialProfileUpdate(BaseModel):
    currency: str | None = None
    salary_day: int | None = None
    onboarding_complete: bool | None = None


class FinancialProfileResponse(BaseModel):
    id: str
    user_id: str
    currency: str
    salary_day: int
    onboarding_complete: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Income Source Schemas ──────────────────────────────────────────────────

class IncomeSourceCreate(BaseModel):
    name: str
    amount: float
    type: str = "salary"  # salary, freelance, investment, other


class IncomeSourceUpdate(BaseModel):
    name: str | None = None
    amount: float | None = None
    type: str | None = None


class IncomeSourceResponse(BaseModel):
    id: str
    user_id: str
    name: str
    amount: float
    type: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Fixed Expense Schemas ───────────────────────────────────────────────────

class FixedExpenseCreate(BaseModel):
    name: str
    amount: float
    category: str  # housing, food, transport, bills, subscriptions


class FixedExpenseUpdate(BaseModel):
    name: str | None = None
    amount: float | None = None
    category: str | None = None


class FixedExpenseResponse(BaseModel):
    id: str
    user_id: str
    name: str
    amount: float
    category: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Debt Schemas ────────────────────────────────────────────────────────────

class DebtCreate(BaseModel):
    name: str
    total_amount: float
    remaining_amount: float
    interest_rate: float = 0.0
    payment_per_month: float = 0.0
    start_date: datetime


class DebtUpdate(BaseModel):
    name: str | None = None
    total_amount: float | None = None
    remaining_amount: float | None = None
    interest_rate: float | None = None
    payment_per_month: float | None = None


class DebtResponse(BaseModel):
    id: str
    user_id: str
    name: str
    total_amount: float
    remaining_amount: float
    interest_rate: float
    payment_per_month: float
    start_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Financial Goal Schemas ───────────────────────────────────────────────────

class FinancialGoalCreate(BaseModel):
    name: str
    target_amount: float
    saved_amount: float = 0.0
    deadline: datetime
    category: str = "education"


class FinancialGoalUpdate(BaseModel):
    name: str | None = None
    target_amount: float | None = None
    saved_amount: float | None = None
    deadline: datetime | None = None
    category: str | None = None


class FinancialGoalResponse(BaseModel):
    id: str
    user_id: str
    name: str
    target_amount: float
    saved_amount: float
    deadline: datetime
    category: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Dashboard Stats ──────────────────────────────────────────────────────────

class DashboardStatsResponse(BaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    total_debt: float
    savings_rate: float
    num_accounts: int
    num_transactions: int
