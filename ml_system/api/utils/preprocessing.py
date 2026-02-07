import pandas as pd
from typing import Dict, Any

def dataframe_from_dict(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Converts a single dictionary input into a DataFrame 
    suitable for scikit-learn pipelines.
    """
    # Create DataFrame from single record
    df = pd.DataFrame([data])
    return df
