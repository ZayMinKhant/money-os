from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, FixedExpense
from app.schemas.schemas import (
    FixedExpenseCreate,
    FixedExpenseUpdate,
    FixedExpenseResponse,
)

router = APIRouter(prefix="/fixed-expenses", tags=["fixed-expenses"])


@router.get("/", response_model=list[FixedExpenseResponse])
async def get_fixed_expenses(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all fixed expenses for the current user."""
    result = await db.execute(
        select(FixedExpense).where(FixedExpense.user_id == user.id)
    )
    return result.scalars().all()


@router.post("/", response_model=FixedExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_fixed_expense(
    expense_data: FixedExpenseCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new fixed expense."""
    expense = FixedExpense(**expense_data.model_dump(), user_id=user.id)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


@router.put("/{expense_id}", response_model=FixedExpenseResponse)
async def update_fixed_expense(
    expense_id: str,
    update_data: FixedExpenseUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a fixed expense."""
    result = await db.execute(
        select(FixedExpense).where(
            FixedExpense.id == expense_id,
            FixedExpense.user_id == user.id,
        )
    )
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Fixed expense not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(expense, field, value)

    await db.commit()
    await db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fixed_expense(
    expense_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a fixed expense."""
    result = await db.execute(
        select(FixedExpense).where(
            FixedExpense.id == expense_id,
            FixedExpense.user_id == user.id,
        )
    )
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Fixed expense not found")

    await db.delete(expense)
    await db.commit()
