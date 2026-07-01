from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, IncomeSource
from app.schemas.schemas import (
    IncomeSourceCreate,
    IncomeSourceUpdate,
    IncomeSourceResponse,
)

router = APIRouter(prefix="/income", tags=["income"])


@router.get("/", response_model=list[IncomeSourceResponse])
async def get_income_sources(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all income sources for the current user."""
    result = await db.execute(
        select(IncomeSource).where(IncomeSource.user_id == user.id)
    )
    return result.scalars().all()


@router.post("/", response_model=IncomeSourceResponse, status_code=status.HTTP_201_CREATED)
async def create_income_source(
    income_data: IncomeSourceCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new income source."""
    income = IncomeSource(**income_data.model_dump(), user_id=user.id)
    db.add(income)
    await db.commit()
    await db.refresh(income)
    return income


@router.put("/{income_id}", response_model=IncomeSourceResponse)
async def update_income_source(
    income_id: str,
    update_data: IncomeSourceUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an income source."""
    result = await db.execute(
        select(IncomeSource).where(
            IncomeSource.id == income_id,
            IncomeSource.user_id == user.id,
        )
    )
    income = result.scalar_one_or_none()
    if not income:
        raise HTTPException(status_code=404, detail="Income source not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(income, field, value)

    await db.commit()
    await db.refresh(income)
    return income


@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_income_source(
    income_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an income source."""
    result = await db.execute(
        select(IncomeSource).where(
            IncomeSource.id == income_id,
            IncomeSource.user_id == user.id,
        )
    )
    income = result.scalar_one_or_none()
    if not income:
        raise HTTPException(status_code=404, detail="Income source not found")

    await db.delete(income)
    await db.commit()
