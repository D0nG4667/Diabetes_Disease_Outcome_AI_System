import pandas as pd
import logging
from schemas.patient import Patient
from sklearn.pipeline import Pipeline
from typing import Optional

logger = logging.getLogger(__name__)

def preprocess_input(patient_data: Patient, feature_creator: Optional[Pipeline]=None, preprocessor: Optional[Pipeline]=None):
    """
    Apply feature engineering (pipeline) and scaling (preprocessor).
    """
    # Convert Pydantic model to DataFrame
    input_df = pd.DataFrame([patient_data.model_dump(exclude={'include_shap'})])
    
    # 1. Pipeline (Feature Engineering)
    if feature_creator:
        try:
            # Assuming pipeline transforms dataframe -> dataframe or array
            # If pipeline is just a transformer, we call transform
            # In some setups, you might have custom steps.
            # We'll assume it returns a DataFrame or something compatible with the preprocessor
            input_df = feature_creator.transform(input_df) 
        except Exception as e:
            logger.error(f"Feature creator pipeline transformation failed: {e}")
            raise e
            
    # 2. Preprocessor (Scaling/Encoding)
    if preprocessor:
        try:
            # Preprocessor usually returns numpy array
            processed_data = preprocessor.transform(input_df)
            return processed_data
        except Exception as e:
            logger.error(f"Preprocessor transformation failed: {e}")
            raise e
            
    return input_df.values  # Fallback if no artifacts
