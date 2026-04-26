"""
Demo data router for setting up and managing demo users.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.services.demo_data import setup_demo_data, get_demo_user_info

router = APIRouter(prefix="/api/demo", tags=["demo"])


@router.post("/setup")
def setup_demo():
    """Set up all demo users with comprehensive data."""
    return setup_demo_data()


@router.get("/info")
def demo_info():
    """Get information about demo users and features."""
    return get_demo_user_info()
