from fastapi import APIRouter, HTTPException, Query
from schemas.patient import Patient, ExplanationResponse
from services.explainer import ExplainerService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/explain", response_model=ExplanationResponse, tags=["Explainability"])
async def explain_risk(
    patient: Patient, 
    top_n: int = Query(10, ge=1, le=50, description="Number of top features to return"),
    plot: bool = Query(False, description="Whether to include a base64 plot")
):
    """
    Generate SHAP explanations for a given patient.
    """
    try:
        response = ExplainerService.explain(patient, top_n=top_n, plot=plot)
        return response
    except Exception as e:
        logger.exception("Explanation failed")
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")
