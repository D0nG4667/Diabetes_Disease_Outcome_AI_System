from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.patient import Patient, ExplainResponse
from services.explainer import ExplainerService, get_explainer_service
from core.security import get_api_key

router = APIRouter()

@router.post("/explain", response_model=ExplainResponse, tags=["Explainability"], dependencies=[Depends(get_api_key)])
async def explain(
    patient: Patient,
    top_n: int = Query(10, ge=1, le=50, description="Number of top features to return"),
    plot: bool = Query(False, description="Whether to include a base64 plot"),
    service: ExplainerService = Depends(get_explainer_service)
):
    """
    Generate SHAP values and visualization for model explanation per patient.
    """
    try:
        result = await service.explain(patient, top_n=top_n, plot=plot)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
