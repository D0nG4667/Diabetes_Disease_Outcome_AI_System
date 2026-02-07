import joblib
import pandas as pd
import tensorflow as tf
import logging
import json
from pathlib import Path
from core.config import settings
from core.exceptions import ArtifactLoadError
from utils.temperature_scaling import TemperatureScaler
import requests

logger = logging.getLogger(__name__)

class ModelArtifacts:
    """
    Singleton-like container for ML artifacts.
    Loaded at startup.
    """

    _instance = None
    
    def __init__(self):
        self.feature_creator = None
        self.preprocessor = None
        self.model = None
        self.scaler = None
        self.threshold = 0.5
        self.background_data = None
        self.is_loaded = False

    def download_if_missing(self, path: Path, url: str):
        if not path.exists():
            logger.info(f"Downloading {path.name} from {url}...")
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with requests.get(url, stream=True) as response:
                    response.raise_for_status()
                    with open(path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                logger.info(f"Downloaded {path.name}")
            except Exception as e:
                logger.error(f"Failed to download {path.name}: {e}")
        else:
            logger.info(f"Artifact {path.name} found locally. Skipping download.")

    
    # Singleton pattern
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    def load_artifacts(self):
        """
        Loads all ML artifacts into memory.
        """
        if self.is_loaded:
            logger.info("Artifacts already loaded.")
            return

        logger.info("Loading artifacts...")
        
        # Ensure all artifacts are present
        for path, url in settings.ARTIFACT_URLS.items():
            self.download_if_missing(path, url)

        try:

            # 1. Load Keras Model
            if not settings.model_path_abs.exists():
                logger.warning(f"Model file not found at {settings.model_path_abs}. Skipping load.")
            else:
                # Register custom objects if the model was saved with them or references them
                # Though typical SaveModel format handles layers well, sometimes custom classes need registration
                with tf.keras.utils.custom_object_scope({'TemperatureScaler': TemperatureScaler}):
                     self.model = tf.keras.models.load_model(settings.model_path_abs, compile=False)
                logger.info(f"Keras model loaded from {settings.model_path_abs}.")

            # 2. Load Temperature Scaler
            if not settings.scaler_path_abs.exists():
                logger.warning(f"Scaler file not found at {settings.scaler_path_abs}. Using default initialization.")
                self.scaler = TemperatureScaler() # Default fallback
            else:
                with tf.keras.utils.custom_object_scope({'TemperatureScaler': TemperatureScaler}):
                     self.scaler = tf.keras.models.load_model(settings.scaler_path_abs, compile=False)
                logger.info(f"TemperatureScaler loaded from {settings.scaler_path_abs}.")

            # 3. Load Feature Creator (Pipeline)
            if not settings.feature_creator_path_abs.exists():
                logger.warning(f"Feature Creator file not found at {settings.feature_creator_path_abs}. Skipping load.")
            else:
                self.feature_creator = joblib.load(settings.feature_creator_path_abs)
                logger.info(f"Feature Creator loaded from {settings.feature_creator_path_abs}.")

            # 4. Load Preprocessor
            if not settings.preprocessor_path_abs.exists():
                logger.warning(f"Preprocessor file not found at {settings.preprocessor_path_abs}. Skipping load.")
            else:
                self.preprocessor = joblib.load(settings.preprocessor_path_abs)
                logger.info(f"Preprocessor loaded from {settings.preprocessor_path_abs}.")
            
            # 5. Load Threshold
            if settings.threshold_path_abs.exists():
                try:
                    with open(settings.threshold_path_abs, 'r') as f:
                        data = json.load(f)
                        # Expecting format like {"best_threshold": 0.35} or just a float
                        if isinstance(data, dict) and "best_threshold" in data:
                            self.threshold = float(data["best_threshold"])
                        elif isinstance(data, float):
                            self.threshold = data
                    logger.info(f"Clinical threshold loaded: {self.threshold}")
                except Exception as e:
                    logger.warning(f"Failed to parse threshold file: {e}. Using default 0.5")
            
            # 6. Load Background Data
            if not settings.background_data_path_abs.exists():
                logger.warning(f"Background data not found at {settings.background_data_path_abs}. Skipping load.")
            else:
                self.background_data = pd.read_csv(settings.background_data_path_abs)
                logger.info("Background data loaded.")

            self.is_loaded = True
            logger.info("All artifacts loaded successfully.")

        except Exception as e:
            logger.error(f"Failed to load artifacts: {e}")
            raise ArtifactLoadError(f"Failed to load artifacts: {e}")
    
    def clear(self):
        """
        Unloads all ML artifacts from memory.
        """
        logger.info("Unloading artifacts...")
        self.feature_creator = None
        self.preprocessor = None
        self.model = None
        self.scaler = None
        self.threshold = None
        self.background_data = None
        self.is_loaded = False
        logger.info("Artifacts unloaded.")


# Global instance
def get_artifacts() -> ModelArtifacts:
    return ModelArtifacts.get_instance()
