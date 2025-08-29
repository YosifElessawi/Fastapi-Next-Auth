"""
FastAPI Application Entry Point

This module initializes the FastAPI application
and includes all API routes.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging_config import setup_logging

# Configure logging
logger = setup_logging()

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI project with SQLAlchemy and PostgreSQL",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG,
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API routes here
# from app.api.v1.routers import router as api_router
# app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors and return a formatted response.

    Args:
        request: The request that caused the error
        exc: The validation exception

    Returns:
        JSONResponse: Formatted error response with validation details
    """
    errors = [
        {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]

    logger.error(f"Validation error: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors},
    )


@app.on_event("startup")
async def startup_event() -> None:
    """Run application startup events."""
    logger.info("Application startup")
    # Add any startup events here (e.g., database initialization)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Run application shutdown events."""
    logger.info("Application shutdown")
    # Add any cleanup events here


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint that returns a welcome message.

    Returns:
        dict: A welcome message with API documentation links
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }
