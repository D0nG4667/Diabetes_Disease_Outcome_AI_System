from fastapi import APIRouter, Depends, HTTPException
from schemas.patient import Patient, PredictionResponse
from services.predictor import PredictorService
from core.exceptions import ModelPredictionError
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict", response_model=PredictionResponse, tags=["Inference"])
async def predict_risk(patient: Patient):
    """
    Predict diabetes risk for a given patient.
    """
    try:
        response = PredictorService.predict(patient)
        return response
    except ModelPredictionError as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error in predict endpoint")
        raise HTTPException(status_code=500, detail="Internal inference error")
