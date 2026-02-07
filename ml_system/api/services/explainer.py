import shap
import numpy as np
import logging
from models.artifacts_loader import get_artifacts
from schemas.patient import Patient, ExplanationResponse, SHAPFeature
from utils.preprocessing import dataframe_from_dict
from utils.shap_utils import generate_shap_summary_plot_base64
from datetime import datetime

logger = logging.getLogger(__name__)

class ExplainerService:
    @staticmethod
    def explain(patient: Patient, top_n: int = 10, plot: bool = False) -> ExplanationResponse:
        artifacts = get_artifacts()
        if not artifacts.model:
            raise RuntimeError("Model not loaded")

        try:
            # 1. Prepare Input (reuse logic or extract common preparation)
            # 1. Prepare Input
            input_dict = patient.model_dump(exclude={"include_shap", "shap_plot"})
            X = dataframe_from_dict(input_dict)
            
            # The model is a Pipeline.
            # shap_background is transformed data (30 cols).
            # We must explain the inner classifier using transformed input.
            
            pipeline = artifacts.model
            
            # Heuristic to split pipeline: assume last step is classifier
            # Imblearn/Sklearn pipelines support indexing
            try:
                # Steps before the last one are preprocessing
                preprocessor_steps = pipeline[:-1] 
                classifier = pipeline[-1]
                
                # Transform proper input X (raw) to X_proc (transformed, matching background)
                X_proc = preprocessor_steps.transform(X)
                
            except Exception as e:
                logger.error(f"Failed to split pipeline or transform data: {e}")
                # Fallback: if splitting fails, we can't really proceed if background is transformed
                raise RuntimeError("Could not prepare data for explanation. Model pipeline structure unexpected.")

            # 2. Compute SHAP
            try:
                # Try TreeExplainer on the inner classifier
                explainer = shap.TreeExplainer(classifier)
                shap_values = explainer.shap_values(X_proc)
                
                if isinstance(shap_values, list):
                    shap_vals_target = shap_values[1]
                elif len(np.array(shap_values).shape) == 3 and np.array(shap_values).shape[2] == 2:
                     shap_vals_target = shap_values[1]
                else:
                    shap_vals_target = shap_values

            except Exception as e:
                logger.info(f"TreeExplainer failed ({e}), falling back to KernelExplainer")
                if artifacts.shap_background is None:
                    raise RuntimeError("SHAP background data required for KernelExplainer fallback")
                
                # Use classifier's predict_proba with transformed background
                explainer = shap.KernelExplainer(classifier.predict_proba, artifacts.shap_background)
                shap_values_all = explainer.shap_values(X_proc, nsamples=100)
                
                # Robustly extract positive class values
                if isinstance(shap_values_all, list):
                    # For binary classification, usually [neg, pos]
                    if len(shap_values_all) > 1:
                        shap_vals_target = shap_values_all[1]
                    else:
                         shap_vals_target = shap_values_all[0]
                elif isinstance(shap_values_all, np.ndarray):
                    # Check dimensions
                    # (samples, features, outputs) or (samples, features)
                    if len(shap_values_all.shape) == 3 and shap_values_all.shape[2] > 1:
                         shap_vals_target = shap_values_all[:, :, 1]
                    else:
                         shap_vals_target = shap_values_all
                else:
                    # Fallback assuming it's the target directly
                    shap_vals_target = shap_values_all

            # shap_vals_target is (features,) or (1, features)
            if len(shap_vals_target.shape) == 2:
                sv = shap_vals_target[0]
            else:
                sv = shap_vals_target

            # 3. Features Names
            try:
                feature_names = preprocessor_steps.get_feature_names_out()
            except:
                # fallback
                feature_names = [f"fet_{i}" for i in range(len(sv))]

            # 4. Top Features
            abs_importance = np.abs(sv)
            top_indices = np.argsort(abs_importance)[-top_n:][::-1]
            
            top_features = [
                SHAPFeature(feature=str(feature_names[i]), value=float(sv[i]))
                for i in top_indices
            ]
            
            # 5. Plot
            plot_b64 = None
            if plot:
                plot_b64 = generate_shap_summary_plot_base64(shap_vals_target, X_proc, feature_names)

            return ExplanationResponse(
                top_features=top_features,
                shap_plot_base64=plot_b64,
                metadata={
                    "method": "SHAP",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.exception("Error during explanation")
            raise RuntimeError(f"Explanation failed: {e}")
