import logging
import tensorflow as tf
from models.artifacts_loader import get_artifacts
from schemas.patient import Patient, PredictionResponse
from utils.preprocessing import preprocess_input
from core.exceptions import ModelPredictionError
from datetime import datetime
from core.config import settings

logger = logging.getLogger(__name__)

class PredictorService:
    def __init__(self):
        self.artifacts = get_artifacts()

    async def predict(self, patient: Patient) -> PredictionResponse:
        if not self.artifacts.is_loaded:
            logger.error("Attempted prediction with unload artifacts.")
            raise ModelPredictionError("Model artifacts not loaded")

        try:
            # 1. Preprocess
            # Signature: preprocess_input(patient_data, feature_creator, preprocessor)
            features = preprocess_input(
                patient, 
                feature_creator=self.artifacts.feature_creator, 
                preprocessor=self.artifacts.preprocessor
            )
            
            # 2. Predict (Logits Extraction)
            # The model is "clinical_mlp_classifier" with "probabilities" output.
            # We need the "logits" layer output for the TemperatureScaler.
            
            # Option A: Create a logits extractor model on fly (efficient enough if Keras graph allows)
            # Or Option B: Expect self.artifacts.model to output logits? No, trained model outputs probs.
            # We reconstruct the logits sub-model.
            
            # Check if we already cached a logits model? Maybe not.
            # Creating it every request is slightly overhead (graph construction), but usually fine for Keras execution.
            # For HFT we would cache this.
            
            logits_model = tf.keras.Model(
                inputs=self.artifacts.model.input,
                outputs=self.artifacts.model.get_layer("logits").output
            )
            
            logits = logits_model.predict(features, verbose=0)
            
            # 3. Temp Scale
            # Scaler is a tf.keras.Model
            if self.artifacts.scaler:
                scaled_logits = self.artifacts.scaler(logits)
            else:
                scaled_logits = logits # Fallback
            
            # 4. Probability
            # Apply Sigmoid specifically
            probability = float(tf.sigmoid(scaled_logits).numpy().flatten()[0])
            
            # 5. Threshold
            threshold = self.artifacts.threshold
            outcome = 1 if probability >= threshold else 0
            
            return PredictionResponse(
                probability=probability,
                outcome=outcome,
                threshold=threshold,
                metadata={
                    "model_name": settings.MODEL_FILENAME,
                    "version": settings.VERSION,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            logger.exception("Prediction failed")
            raise ModelPredictionError(str(e))

predictor_service = PredictorService()

def get_predictor_service() -> PredictorService:
    return predictor_service
