import shap
import logging
import numpy as np
from datetime import datetime
from models.artifacts_loader import get_artifacts
from schemas.patient import Patient, ExplainResponse
from utils.preprocessing import preprocess_input
from utils.shap_utils import generate_shap_summary_plot_base64
from core.exceptions import ModelPredictionError

logger = logging.getLogger(__name__)

class ExplainerService:
    def __init__(self):
        self.artifacts = get_artifacts()
        self.explainer = None

    def _get_explainer(self):
        """
        Lazy load explainer to save startup time or handle failures.
        """
        if self.explainer:
            return self.explainer
            
        if not self.artifacts.model or self.artifacts.background_data is None:
            return None
            
        try:
            # Try DeepExplainer
            # Note: DeepExplainer requires the model and background data (numpy array)
            # If background_data is DF, convert to numpy
            bg_data = self.artifacts.background_data
            if hasattr(bg_data, "values"):
                bg_data = bg_data.values
                
            # Usually we pass a summary (kmeans) of background data to speed up
            # e.g. shap.sample(bg_data, 100) or kmeans
            # For now use as is
            
            self.explainer = shap.DeepExplainer(self.artifacts.model, bg_data)
            return self.explainer
        except Exception as e:
            logger.warning(f"DeepExplainer failed initialization: {e}. Falling back to KernelExplainer (not implemented for DL speed reasons usually).")
            # Fallback could go here
            return None

    async def explain(self, patient: Patient, top_n: int = 10, plot: bool = False) -> ExplainResponse:
        if not self.artifacts.is_loaded:
             raise ModelPredictionError("Model artifacts not loaded")

        features = preprocess_input(
            patient, 
            feature_creator=self.artifacts.feature_creator, 
            preprocessor=self.artifacts.preprocessor
        )
        
        explainer = self._get_explainer()
        if not explainer:
            raise ModelPredictionError("SHAP Explainer could not be initialized")
            
        try:
            shap_values = explainer.shap_values(features)
            # shap_values is a list for functional models multi-output, or array.
            
            # Handling 1 output node
            if isinstance(shap_values, list):
                sv = shap_values[0]
            else:
                sv = shap_values
                
            # Top Features
            # sv is (1, n_features)
            sv_flat = sv.flatten()
            feature_names = patient.model_dump(exclude={'include_shap'}).keys()
            
            # Map index to valid feature name if pipeline didn't change feature count/order
            # CAUTION: If pipeline changes features (OneHot), names mismatch.
            # Assuming 1:1 mapping for this prompt's simplicity or strictly numerical input.
            # If mismatch, use "Feature N"
            
            feature_list = list(feature_names)
            if len(feature_list) != len(sv_flat):
                 feature_list = [f"Feature {i}" for i in range(len(sv_flat))]
            
            # Sort by abs value
            indices = np.argsort(-np.abs(sv_flat))[:top_n] # Use user provided top_n
            top_features = [
                {"feature": str(feature_list[i]), "value": float(sv_flat[i])}
                for i in indices
            ]
            
            # Plot
            plot_base64 = None
            if plot:
                # New Plotly utility
                # It expects (shap_values, X, feature_names)
                # shap_values should be just the values for the features (1D array)
                plot_base64 = generate_shap_summary_plot_base64(sv_flat, features, feature_list)
            
            return ExplainResponse(
                top_features=top_features,
                shap_plot_base64=plot_base64,
                metadata={
                    "method": "SHAP",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

        except Exception as e:
            logger.exception("Explanation generation failed")
            raise ModelPredictionError(f"Explanation failed: {e}")

explainer_service = ExplainerService()

def get_explainer_service() -> ExplainerService:
    return explainer_service
