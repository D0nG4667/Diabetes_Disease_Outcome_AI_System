from fastapi import APIRouter, Depends, HTTPException
from schemas.patient import Patient, PredictionResponse
from services.predictor import PredictorService, get_predictor_service
from core.security import get_api_key

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, tags=["prediction"], dependencies=[Depends(get_api_key)])
async def predict(
    patient: Patient,
    service: PredictorService = Depends(get_predictor_service)
):
    """
    Predict diabetes risk based on patient clinical features.
    """
    try:
        if patient.include_shap:
            # Future implementation: verify if we want to merge prediction + explanation
            # For now, we follow strict output separation but acknowledge the flag.
            pass 
            
        result = await service.predict(patient)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
