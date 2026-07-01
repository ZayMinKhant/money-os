from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, Budget
from app.schemas.schemas import (
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse,
)

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("/", response_model=list[BudgetResponse])
async def get_budgets(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all budgets for the current user."""
    result = await db.execute(
        select(Budget).where(Budget.user_id == user.id)
    )
    return result.scalars().all()


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new budget."""
    budget = Budget(**budget_data.model_dump(), user_id=user.id)
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific budget by ID."""
    result = await db.execute(
        select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user.id,
        )
    )
    budget = result.scalar_one_or_none()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    update_data: BudgetUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a budget."""
    result = await db.execute(
        select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user.id,
        )
    )
    budget = result.scalar_one_or_none()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(budget, field, value)

    await db.commit()
    await db.refresh(budget)
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a budget."""
    result = await db.execute(
        select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user.id,
        )
    )
    budget = result.scalar_one_or_none()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    await db.delete(budget)
    await db.commit()
