from models.artifacts_loader import ModelArtifacts
from schemas.patient import Patient, PredictionResponse
from utils.preprocessing import dataframe_from_dict
from core.exceptions import ModelPredictionError
import logging
from datetime import datetime
from core.config import settings

logger = logging.getLogger(__name__)

class PredictorService:
    @staticmethod
    def predict(patient: Patient) -> PredictionResponse:
        artifacts = ModelArtifacts.get_instance()
        if not artifacts.model:
            raise ModelPredictionError("Model not loaded")

        try:
            # 1. Prepare Input
            input_dict = patient.model_dump(exclude={"include_shap", "shap_plot"})
            X = dataframe_from_dict(input_dict)
            
            # 2. Model Prediction
            # The loaded model is a full pipeline that expects the raw DataFrame (features + missing handling internal)
            # So we pass X directly, skipping separate preprocessor artifacts if they suggest otherwise.
            proba = float(artifacts.model.predict_proba(X)[:, 1].ravel()[0])
            
            # 3. Thresholding
            threshold = artifacts.threshold
            outcome = int(proba >= threshold)
            
            return PredictionResponse(
                probability=proba,
                outcome=outcome,
                threshold=threshold,
                metadata={
                    "model_name": settings.MODEL_FILENAME,
                    "version": settings.VERSION,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

        except Exception as e:
            logger.exception("Error during prediction")
            raise ModelPredictionError(str(e))
