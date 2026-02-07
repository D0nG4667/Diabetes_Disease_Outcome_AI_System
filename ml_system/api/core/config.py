from pathlib import Path
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings

# Define Paths
# Using __file__ to reliably get the project root.
# api/core/config.py -> api/core -> api -> ml_system (root) -> ml_system/api
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# ENV when using standalone uvicorn server running FastAPI in api directory
ENV_PATH = Path(".env")

DATASET_DIR = BASE_DIR / "data"
RAW_DIR = DATASET_DIR / "raw"
TRAIN_TEST = RAW_DIR / "kaggle/diabetes.csv"

PROCESSED_DIR = DATASET_DIR / "processed"
TRAIN_TEST_PROCESSED = PROCESSED_DIR / "diabetes.csv"

PLOTS = BASE_DIR / "plots"
SAVE_MODELS = BASE_DIR / "models"
ML_MODELS = SAVE_MODELS / "ml"

EDA_ARTIFACTS = BASE_DIR / "artifacts" / "eda"
PREPROCESSING_ARTIFACTS = BASE_DIR / "artifacts" / "preprocessing"
ML_ARTIFACTS = BASE_DIR / "artifacts" / "ml"
DL_ARTIFACTS = BASE_DIR / "artifacts" / "dl"

DESCRIPTION = """
This API identifies patients at risk of developing type 2 diabetes (diabetes mellitus) - a chronic condition that occurs when the body's cells become resistant to insulin or when the body doesn't produce enough insulin.\n
 
### Results 
**Diabetes Outcome:** *1 or Yes or High risk* if a patient will develop a type 2 diabetes, and *0 or No or Low risk* otherwise\n

**Diabetes probability:** Estimated risk percentage (0-100%)\n

### Let's Connect
### Connect
👨‍⚕️ `Gabriel Okundaye`\n
[<img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" width="20" height="20">  LinkendIn](https://www.linkedin.com/in/dr-gabriel-okundaye)

[<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="20" height="20">  GitHub](https://github.com/D0nG4667/)
"""

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Diabetes Risk Prediction API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = DESCRIPTION
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Directories (kept as Path objects)
    MODEL_DIR: Path = ML_MODELS
    ARTIFACTS_DIR: Path = ML_ARTIFACTS
    
    # Filenames
    MODEL_FILENAME: str = "XGBClassifier__RandomUnderSampler.joblib"
    THRESHOLD_FILENAME: str = "ml_threshold.json"
    SHAP_BACKGROUND_FILENAME: str = "shap_background.joblib"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()