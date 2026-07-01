from fastapi import APIRouter

from app.api.dashboard import router as dashboard_router
from app.api.transactions import router as transactions_router
from app.api.accounts import router as accounts_router
from app.api.budgets import router as budgets_router
from app.api.profile import router as profile_router
from app.api.income import router as income_router
from app.api.fixed_expenses import router as fixed_expenses_router

api_router = APIRouter()

api_router.include_router(dashboard_router)
api_router.include_router(transactions_router)
api_router.include_router(accounts_router)
api_router.include_router(budgets_router)
api_router.include_router(profile_router)
api_router.include_router(income_router)
api_router.include_router(fixed_expenses_router)
