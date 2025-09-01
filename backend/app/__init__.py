"""
FastAPI Application Package

This package contains the main FastAPI application and its components.
"""

__version__ = "0.1.0"

# Import all models here so they're properly registered with SQLAlchemy
from app.todo.models import todo  # noqa
from app.user.models import user  # noqa
