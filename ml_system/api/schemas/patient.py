from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict

# Future implementation: add constraints to the features using min max of the dataset
class Patient(BaseModel):
    pregnancies: int = Field(..., ge=0, description="Number of times pregnant")
    glucose: float = Field(..., ge=0, description="Plasma glucose concentration")
    blood_pressure: float = Field(..., ge=0, description="Diastolic blood pressure (mm Hg)")
    skin_thickness: float = Field(..., ge=0, description="Triceps skin fold thickness (mm)")
    insulin: float = Field(..., ge=0, description="2-Hour serum insulin (mu U/ml)")
    bmi: float = Field(..., ge=0, description="Body mass index")
    diabetes_pedigree_function: float = Field(..., ge=0, description="Diabetes pedigree function")
    age: int = Field(..., ge=0, description="Age (years)")
    
    # Optional flags for SHAP
    include_shap: Optional[bool] = Field(False, description="Whether to include SHAP explanation in prediction response (deprecated, use /explain)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pregnancies": 6,
                "glucose": 148,
                "blood_pressure": 72,
                "skin_thickness": 35,
                "insulin": 3,
                "bmi": 33.6,
                "diabetes_pedigree_function": 0.627,
                "age": 50
            }
        }

class PredictionResponse(BaseModel):
    probability: float
    outcome: int
    threshold: float
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SHAPFeature(BaseModel):
    feature: str
    value: float

class ExplanationResponse(BaseModel):
    top_features: List[SHAPFeature]
    shap_plot_base64: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
