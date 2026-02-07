from fastapi import APIRouter
from core.config import settings
from models.artifacts_loader import get_artifacts

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify service status.
    """
    artifacts = get_artifacts()
    status = "healthy" if artifacts.is_loaded else "degraded"
    return {
        "status": status,
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "artifacts_loaded": artifacts.is_loaded,
        "model_loaded": artifacts.model is not None,
        "shap_background_loaded": artifacts.shap_background is not None
    }
