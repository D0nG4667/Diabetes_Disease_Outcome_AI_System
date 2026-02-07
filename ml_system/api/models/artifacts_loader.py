import joblib
import json
import logging
from typing import Any, Optional
from sklearn.pipeline import Pipeline
from core.config import settings
from core.exceptions import ArtifactLoadError

logger = logging.getLogger(__name__)

class ModelArtifacts:
    """
    Singleton-like container for ML artifacts.
    Loaded at startup.
    """
    _instance = None
    
    def __init__(self):
        self.model: Optional[Pipeline] = None
        self.threshold: float = 0.5
        self.shap_background: Any = None
        self.feature_names: Optional[list] = None
        self.is_loaded = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_artifacts(self):
        """
        Loads all artifacts from disk into memory.
        """        
        if self.is_loaded:
            logger.info("Artifacts already loaded.")
            return

        # Directories are now Path objects
        model_dir = settings.MODEL_DIR
        artifacts_dir = settings.ARTIFACTS_DIR

        logger.info(f"Loading models from {model_dir}")
        logger.info(f"Loading artifacts from {artifacts_dir}")
        
        try:
            # Load Model
            model_path = model_dir / settings.MODEL_FILENAME
            if model_path.exists():
                self.model = joblib.load(model_path)
                logger.info(f"Loaded model from {model_path}")
            else:
                logger.error(f"Model file not found at {model_path}")
                raise FileNotFoundError(f"Model not found at {model_path}")

            # Load Threshold
            thresh_path = artifacts_dir / settings.THRESHOLD_FILENAME
            if thresh_path.exists():
                with open(thresh_path, 'r') as f:
                    data = json.load(f)
                    self.threshold = float(data.get("threshold", 0.5))
                logger.info(f"Loaded threshold {self.threshold} from {thresh_path}")
            else:
                logger.warning(f"Threshold file not found at {thresh_path}, using default 0.5")

            # Load SHAP Background
            shap_path = artifacts_dir / settings.SHAP_BACKGROUND_FILENAME
            if shap_path.exists():
                self.shap_background = joblib.load(shap_path)
                logger.info(f"Loaded SHAP background from {shap_path}")
            else:
                logger.warning(f"SHAP background not found at {shap_path}, SHAP explanations might fail.")

            self.is_loaded = True
            logger.info("All artifacts loaded successfully.")
                
        except Exception as e:
            logger.error(f"Failed to load artifacts: {e}")
            raise ArtifactLoadError(f"Critical error loading artifacts: {e}")

    def clear(self):
        """
        Unloads all ML artifacts from memory.
        """
        logger.info("Unloading artifacts...")
        self.model = None
        self.threshold = None
        self.shap_background = None
        self.is_loaded = False
        logger.info("Artifacts unloaded.")

# Global instance
artifacts = ModelArtifacts()

def get_artifacts() -> ModelArtifacts:
    return artifacts