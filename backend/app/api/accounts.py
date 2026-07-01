from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, Account
from app.schemas.schemas import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountResponse])
async def get_accounts(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all accounts for the current user."""
    result = await db.execute(
        select(Account).where(Account.user_id == user.id)
    )
    return result.scalars().all()


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new account."""
    account = Account(**account_data.model_dump(), user_id=user.id)
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific account by ID."""
    result = await db.execute(
        select(Account).where(
            Account.id == account_id,
            Account.user_id == user.id,
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    update_data: AccountUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an account."""
    result = await db.execute(
        select(Account).where(
            Account.id == account_id,
            Account.user_id == user.id,
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(account, field, value)

    await db.commit()
    await db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an account."""
    result = await db.execute(
        select(Account).where(
            Account.id == account_id,
            Account.user_id == user.id,
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    await db.delete(account)
    await db.commit()
