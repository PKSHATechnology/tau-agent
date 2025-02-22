"""API endpoints for the tau agent."""

from fastapi import APIRouter

from tau.api.ask_agent import router as ask_agent_router
from tau.api.create_agent import router as create_agent_router
from tau.api.end_agent import router as end_agent_router
from tau.api.healthz import router as healthz_router

router = APIRouter()
router.include_router(healthz_router)
router.include_router(create_agent_router)
router.include_router(end_agent_router)
router.include_router(ask_agent_router)
