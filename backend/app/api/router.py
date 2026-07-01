from fastapi import APIRouter

from app.api.dashboard import router as dashboard_router
from app.api.transactions import router as transactions_router
from app.api.accounts import router as accounts_router
from app.api.budgets import router as budgets_router

api_router = APIRouter()

api_router.include_router(dashboard_router)
api_router.include_router(transactions_router)
api_router.include_router(accounts_router)
api_router.include_router(budgets_router)
