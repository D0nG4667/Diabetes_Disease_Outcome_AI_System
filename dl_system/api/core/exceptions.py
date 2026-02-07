from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class ModelPredictionError(Exception):
    """Raised when model prediction fails."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

class ArtifactLoadError(Exception):
    """Raised when artifacts fail to load."""
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for HTTP exceptions to ensure JSON response.
    """
    logger.error(f"HTTPException: {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler for unhandled errors.
    """
    logger.exception(f"Unhandled exception: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please check logs for more details."},
    )

async def model_prediction_exception_handler(request: Request, exc: ModelPredictionError):
    logger.error(f"Model prediction error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error performing model prediction."},
    )
