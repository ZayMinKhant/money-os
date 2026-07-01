from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from clerk_backend_sdk import Clerk
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db

settings = get_settings()
security = HTTPBearer()
clerk = Clerk(bearer_auth=settings.clerk_secret_key)


async def verify_clerk_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify Clerk JWT token and return the token payload."""
    try:
        token = credentials.credentials
        payload = clerk.verify_token(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


async def get_current_user(
    payload: dict = Depends(verify_clerk_token),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user from Clerk payload and sync with our database."""
    from app.models.models import User
    from sqlalchemy import select

    clerk_id = payload.get("sub")
    email = payload.get("email")
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")

    if not clerk_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # Check if user exists in our DB
    result = await db.execute(select(User).where(User.clerk_id == clerk_id))
    user = result.scalar_one_or_none()

    if not user:
        # Create user in our DB on first login
        user = User(
            clerk_id=clerk_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
