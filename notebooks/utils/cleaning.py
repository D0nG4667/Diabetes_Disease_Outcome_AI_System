import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator, TransformerMixin


# Apply snake_case conversion
def to_snake_case(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize all column names of a pandas DataFrame to snake_case format,
    including proper handling of CamelCase and PascalCase patterns.

    This function performs the following transformations on column names:
    1. Inserts underscores between lowercase–uppercase boundaries to split CamelCase/PascalCase
       (e.g., 'BloodPressure' → 'Blood_Pressure').
    2. Converts all characters to lowercase.
    3. Replaces spaces, slashes, hyphens, and parentheses with underscores.
    4. Removes any remaining non-alphanumeric characters except underscores.
    5. Strips leading and trailing underscores.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame whose column names will be standardized.

    Returns
    -------
    pd.DataFrame
        DataFrame with column names converted to snake_case.

    Example
    -------
    >>> df = pd.DataFrame(columns=['BloodPressure', 'Body Weight', 'Race/Ethnicity'])
    >>> df = to_snake_case(df)
    >>> df.columns
    Index(['blood_pressure', 'body_weight', 'race_ethnicity'], dtype='object')
    """
    df = df.copy(deep=True)

    df.columns = (
        df.columns.str.replace(
            r"(?<=[a-z0-9])(?=[A-Z])", "_", regex=True
        )  # Split CamelCase/PascalCase
        .str.lower()  # Convert to lowercase
        .str.replace(r"[\s/()-]+", "_", regex=True)  # Replace separators with '_'
        .str.replace(r"[^0-9a-z_]", "", regex=True)  # Remove invalid characters
        .str.strip("_")  # Trim leading/trailing '_'
    )
    return df


def handle_missing(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
    """
    Clean and impute missing values in the Pima Indians Diabetes dataset.

    This function handles the well‑known issue of *hidden missingness* in the dataset,
    where physiologically impossible zeros appear in several clinical variables.
    It performs the following steps:

    1. Identifies features where zero values represent missing data.
    2. Creates binary missingness indicator columns (e.g., `glucose_missing`).
    3. Replaces zero values with NaN for proper imputation.
    4. Applies the chosen imputation strategy (default: median).
    5. Returns a clean, modeling‑ready DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The diabetes dataset containing columns:
        ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
         'insulin', 'bmi', 'diabetes_pedigree_function', 'age', 'outcome']

    strategy : str, optional
        Imputation strategy to use. Options:
        - "median"  (default)
        - "mean"
        - "most_frequent"

    Returns
    -------
    pd.DataFrame
        A cleaned DataFrame with:
        - Zero‑value missingness corrected
        - Missingness indicator columns added
        - Imputed numeric values
    """

    df = df.copy()

    # Columns where zero is physiologically impossible → treat as missing
    zero_as_missing = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]

    # 1. Create missingness indicator columns
    for col in zero_as_missing:
        df[f"{col}_missing"] = (df[col] == 0).astype(int)

    # 2. Replace zeros with NaN for proper imputation
    df[zero_as_missing] = df[zero_as_missing].replace(0, np.nan)

    # 3. Apply chosen imputation strategy
    imputer = SimpleImputer(strategy=strategy)
    df[zero_as_missing] = imputer.fit_transform(df[zero_as_missing])

    return df


def handle_missing_eda(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the diabetes dataset for Exploratory Data Analysis (EDA) by
    identifying and exposing hidden missingness without performing imputation.

    In the Pima Indians Diabetes dataset, several clinical measurements use
    the value '0' to represent missing or unrecorded data. During EDA, these
    zeros must be surfaced as NaN to avoid misleading statistical summaries
    and distorted visualizations.

    This function performs the following steps:

    1. Identifies features where zero values are physiologically impossible.
    2. Creates binary missingness indicator columns (e.g., `glucose_missing`).
    3. Replaces zero values with NaN for accurate EDA.
    4. Returns the dataset WITHOUT any imputation.

    Parameters
    ----------
    df : pd.DataFrame
        The diabetes dataset containing columns:
        ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
         'insulin', 'bmi', 'diabetes_pedigree_function', 'age', 'outcome']

    Returns
    -------
    pd.DataFrame
        A DataFrame suitable for EDA with:
        - Zero-based missingness exposed as NaN
        - Missingness indicator columns added
        - No imputation performed
    """

    df = df.copy()

    # Columns where zero is physiologically impossible → treat as missing
    zero_as_missing = ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]

    # 1. Add missingness indicator columns
    for col in zero_as_missing:
        df[f"{col}_missing"] = (df[col] == 0).astype(bool)

    # 2. Replace zeros with NaN for EDA
    df[zero_as_missing] = df[zero_as_missing].replace(0, np.nan)

    # 3. Return dataset WITHOUT imputation
    return df


class MissingHandler(BaseEstimator, TransformerMixin):
    """
    A scikit-learn compatible transformer for handling hidden missingness
    in the Pima Indians Diabetes dataset.


    This transformer:
    - Accepts a column→strategy mapping (e.g., {"glucose": "median", "insulin": "mean"}).
    - Identifies features where zero values represent missing data.
    - Creates binary missingness indicator columns (e.g., `glucose_missing`).
    - Replaces zero values with NaN.
    - Applies per-column imputation strategies.
    - Returns a clean, modeling-ready DataFrame.

    Parameters
    ----------
    col_strategy_map : dict
        A dictionary mapping column names to imputation strategies.
        Example:
            {
                "glucose": "median",
                "blood_pressure": "mean",
                "insulin": "median",
                "bmi": "median"
            }

    Attributes
    ----------
    imputers_ : dict
        A dictionary mapping each column to its fitted SimpleImputer.
    """

    def __init__(self, col_strategy_map: dict):
        self.col_strategy_map = col_strategy_map
        self.imputers_ = {}

    def fit(self, X, y=None):
        """
        Fit imputers for each column based on the provided strategy map.

        Parameters
        ----------
        X : pd.DataFrame
            Input dataset.

        y : None
            Ignored (sklearn compatibility).

        Returns
        -------
        self
        """
        X = X.copy()

        for col, strategy in self.col_strategy_map.items():
            # Replace zeros with NaN for fitting
            X[col] = X[col].replace(0, np.nan)

            # Create and fit imputer for this column
            imputer = SimpleImputer(strategy=strategy)
            imputer.fit(X[[col]])

            # Store fitted imputer
            self.imputers_[col] = imputer

        return self

    def transform(self, X):
        """
        Apply missingness handling and per-column imputation.

        Parameters
        ----------
        X : pd.DataFrame

        Returns
        -------
        pd.DataFrame
            Transformed dataset with:
            - Missingness flags
            - Zero→NaN replacement
            - Per-column imputation
        """
        X = X.copy()

        for col, imputer in self.imputers_.items():
            # Add missingness indicator
            X[f"{col}_missing"] = (X[col] == 0).astype(int)

            # Replace zeros with NaN
            X[col] = X[col].replace(0, np.nan)

            # Apply imputation
            X[[col]] = imputer.transform(X[[col]])

        return X
