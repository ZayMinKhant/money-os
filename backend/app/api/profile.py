from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, FinancialProfile
from app.schemas.schemas import (
    FinancialProfileCreate,
    FinancialProfileUpdate,
    FinancialProfileResponse,
)

router = APIRouter(prefix="/profile", tags=["financial-profile"])


@router.get("/", response_model=FinancialProfileResponse)
async def get_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's financial profile."""
    result = await db.execute(
        select(FinancialProfile).where(FinancialProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Financial profile not found. Please complete onboarding.")
    return profile


@router.post("/", response_model=FinancialProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: FinancialProfileCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a financial profile (onboarding)."""
    result = await db.execute(
        select(FinancialProfile).where(FinancialProfile.user_id == user.id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Financial profile already exists")

    profile = FinancialProfile(**profile_data.model_dump(), user_id=user.id)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.put("/", response_model=FinancialProfileResponse)
async def update_profile(
    update_data: FinancialProfileUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update the financial profile."""
    result = await db.execute(
        select(FinancialProfile).where(FinancialProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Financial profile not found")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)
    return profile


@router.patch("/complete-onboarding", response_model=FinancialProfileResponse)
async def complete_onboarding(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark onboarding as complete."""
    result = await db.execute(
        select(FinancialProfile).where(FinancialProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Financial profile not found")

    profile.onboarding_complete = True
    await db.commit()
    await db.refresh(profile)
    return profile
