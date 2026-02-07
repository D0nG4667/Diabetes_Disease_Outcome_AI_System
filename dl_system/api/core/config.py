from pathlib import Path
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define Paths
# Using __file__ to reliably get the project root.
# api/core/config.py -> api/core -> api -> dl_system (root) -> dl_system/api

# Let's assume the user wants the root of the "system" which is usually where artifacts might be or one level up.
# Previous BASE_DIR was 'api' folder. ARTIFACTS_DIR was sibling to 'api'.
# api/core/config.py -> api/core -> api
ROOT_DIR = Path(__file__).resolve().parent.parent

NAMING_CONVENTION = "Deep Learning Diabetes Risk Prediction System"

DESCRIPTION = """
This API identifies patients at risk of developing type 2 diabetes (diabetes mellitus) using a Deep Learning model.
It provides endpoints for prediction and SHAP-based model explanation.

### Key Features
- **Deep Learning Prediction**: Uses a TensorFlow/Keras model.
- **Model Explanation**: Integrated SHAP (SHapley Additive exPlanations) values.
- **Temperature Scaling**: Calibrated probabilities.

### Results 
**Diabetes Outcome:** *1 or Yes or High risk* if a patient will develop a type 2 diabetes, and *0 or No or Low risk* otherwise\n

**Diabetes Probability:** Estimated risk percentage (0-100%)\n

### Connect
👨‍⚕️ `Gabriel Okundaye`\n
[<img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" width="20" height="20">  LinkedIn](https://www.linkedin.com/in/dr-gabriel-okundaye)
[<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="20" height="20">  GitHub](https://github.com/D0nG4667/)
"""

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Diabetes Risk Prediction API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = DESCRIPTION
    
    # Security
    API_KEY: str = "pneumonoultramicroscopicsilicovolcanoconiosis" # Change in production
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Paths
    # We define base directories as Path objects
    BASE_DIR: Path = ROOT_DIR
    # These paths are relative to the API root
    ARTIFACTS_DIR: Path = BASE_DIR / "artifacts/dl"
    MODEL_DIR: Path = BASE_DIR / "models/dl"
    
    # Filenames
    MODEL_FILENAME: str = "best_clinical_mlp_classifier_optuna.keras"
    PREPROCESSOR_FILENAME: str = "preprocessor.joblib"
    FEATURE_CREATOR_FILENAME: str = "feature_creator.joblib"
    SCALER_FILENAME: str = "temperature_scaler.keras"
    THRESHOLD_FILENAME: str = "dl_threshold.json"
    BACKGROUND_DATA_FILENAME: str = "background_data.csv"
    
    # Github URL
    GITHUB_RAW_URL_BASE: str = "https://github.com/D0nG4667/Diabetes_Disease_Outcome_AI_System/raw/main"

    @property
    def ARTIFACT_URLS(self):
        """Map local path properties to their remote URLs"""
        return {
            self.model_path_abs: f"{self.GITHUB_RAW_URL_BASE}/models/dl/{self.MODEL_FILENAME}",
            self.scaler_path_abs: f"{self.GITHUB_RAW_URL_BASE}/models/dl/{self.SCALER_FILENAME}",
            self.preprocessor_path_abs: f"{self.GITHUB_RAW_URL_BASE}/models/dl/{self.PREPROCESSOR_FILENAME}",
            self.feature_creator_path_abs: f"{self.GITHUB_RAW_URL_BASE}/models/dl/{self.FEATURE_CREATOR_FILENAME}",
            self.threshold_path_abs: f"{self.GITHUB_RAW_URL_BASE}/artifacts/dl/{self.THRESHOLD_FILENAME}",
            self.background_data_path_abs: f"{self.GITHUB_RAW_URL_BASE}/artifacts/dl/{self.BACKGROUND_DATA_FILENAME}",
        }

    
    @property
    def model_path_abs(self) -> Path:
        return self.MODEL_DIR / self.MODEL_FILENAME

    @property
    def scaler_path_abs(self) -> Path:
        return self.MODEL_DIR / self.SCALER_FILENAME

    @property
    def preprocessor_path_abs(self) -> Path:
        return self.MODEL_DIR / self.PREPROCESSOR_FILENAME
        
    @property
    def feature_creator_path_abs(self) -> Path:
        return self.MODEL_DIR / self.FEATURE_CREATOR_FILENAME

    @property
    def threshold_path_abs(self) -> Path:
        return self.ARTIFACTS_DIR / self.THRESHOLD_FILENAME

    @property
    def background_data_path_abs(self) -> Path:
        return self.ARTIFACTS_DIR / self.BACKGROUND_DATA_FILENAME

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        case_sensitive=True
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
