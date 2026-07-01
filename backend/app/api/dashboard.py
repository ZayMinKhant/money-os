from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, Account, Transaction, Budget, Debt
from app.schemas.schemas import DashboardStatsResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get aggregated dashboard statistics for the current user."""
    # Total balance across all accounts
    balance_result = await db.execute(
        select(func.coalesce(func.sum(Account.balance), 0)).where(
            Account.user_id == user.id
        )
    )
    total_balance = float(balance_result.scalar())

    # Monthly income
    income_result = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user.id,
            Transaction.type == "income",
            extract("month", Transaction.date) == 7,  # Current month (July)
            extract("year", Transaction.date) == 2026,
        )
    )
    monthly_income = float(income_result.scalar())

    # Monthly expenses
    expense_result = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user.id,
            Transaction.type == "expense",
            extract("month", Transaction.date) == 7,
            extract("year", Transaction.date) == 2026,
        )
    )
    monthly_expenses = float(expense_result.scalar())

    # Total debt
    debt_result = await db.execute(
        select(func.coalesce(func.sum(Debt.remaining_amount), 0)).where(
            Debt.user_id == user.id
        )
    )
    total_debt = float(debt_result.scalar())

    # Savings rate
    savings_rate = 0.0
    if monthly_income > 0:
        savings_rate = round(
            ((monthly_income - monthly_expenses) / monthly_income) * 100, 1
        )

    # Count accounts and transactions
    accounts_count = await db.execute(
        select(func.count(Account.id)).where(Account.user_id == user.id)
    )
    transactions_count = await db.execute(
        select(func.count(Transaction.id)).where(Transaction.user_id == user.id)
    )

    return DashboardStatsResponse(
        total_balance=total_balance,
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        total_debt=total_debt,
        savings_rate=savings_rate,
        num_accounts=int(accounts_count.scalar()),
        num_transactions=int(transactions_count.scalar()),
    )
