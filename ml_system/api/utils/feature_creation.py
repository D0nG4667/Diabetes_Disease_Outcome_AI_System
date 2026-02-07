import numpy as np
import pandas as pd
from typing import List, Dict, Optional
from sklearn.base import BaseEstimator, TransformerMixin
from pandas.api.types import is_numeric_dtype, is_object_dtype

from utils.constants import DEFAULT_COL_MAP


class FeatureCreation(BaseEstimator, TransformerMixin):
    """
    Clinically grounded feature creation for diabetes outcome modeling.

    This transformer performs:
    --------------------------------------------------------------
    1. Missing-value handling (modeling phase only)
       Supported strategies:
         - "median"         → numeric only
         - "mean"           → numeric only
         - "most_frequent"  → categorical only
         - "unknown"        → fill categorical with "Unknown"
         - "none"           → fill categorical with "None"
         - None             → skip imputation

    2. Clinical binning (categorical transformations)
       - Glucose: low / normal / prediabetic / diabetic
       - Pregnancies: nulliparous / uniparous / multiparous / grand / great-grand multiparous
       - Blood pressure: normal/elevated / stage1 / stage2
       - BMI: underweight / normal / overweight / obese
       - Age: young / middle-aged / older adult
       - Skin thickness: cohort-relative (25th–75th percentiles)
       - Insulin: cohort-relative (25th–75th percentiles)

    3. Interaction terms (numeric × numeric)
       - glucose × bmi
       - insulin × skin_thickness
       - age × diabetes_pedigree_function
       - pregnancies × glucose
       - pregnancies × bmi
       - pregnancies × age

    4. Schema locking
       - After fit(), the transformer remembers the full output schema.
       - transform() always returns columns in the same order.
       - Missing columns are added as NaN to maintain consistency.

    This transformer is intended for the **modeling phase**, not EDA.
    """

    def __init__(
        self,
        col_map: Optional[Dict[str, str]] = None,
        drop_cols: Optional[List[str]] = None,
        create_bins: bool = True,
        create_interactions: bool = True,
    ):
        """
        Parameters
        ----------
        col_map : dict
            Mapping of column → missing-value strategy.
            If None, DEFAULT_COL_MAP is used.

        drop_cols : list
            Raw columns to drop after features are created.

        create_bins : bool
            Whether to generate clinical binning features.

        create_interactions : bool
            Whether to generate interaction features.
        """
        self.col_map = col_map
        self.drop_cols = drop_cols
        self.create_bins = create_bins
        self.create_interactions = create_interactions

    # ---------------------------------------------------------
    # Missing handling
    # ---------------------------------------------------------
    def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply missing-value strategies defined in col_map.

        Enhancements:
        - Adds a missingness indicator column *before* imputation.
        For each column 'col', creates: col + "_missing"
        This captures:
            * True missing values (NaN)
            * Zero-as-missing patterns for clinical numeric fields

        Rules:
        - "median" and "mean" → numeric only
        - "most_frequent" → categorical only
        - "unknown" / "none" → categorical only
        - None → skip
        """
        df = df.copy()
        if self.col_map is None:
            return df

        for col, strategy in self.col_map.items():
            if col not in df.columns or strategy is None:
                continue

            col_is_numeric = is_numeric_dtype(df[col])
            col_is_categorical = (
                is_object_dtype(df[col]) or df[col].dtype.name == "category"
            )

            # ---------------------------------------------------------
            # 1. Add missingness flag BEFORE filling
            # ---------------------------------------------------------
            # For numeric clinical variables, zeros often represent missingness.
            if col_is_numeric:
                df[f"{col}_missing"] = df[col].isna() | (df[col] == 0)
            else:
                df[f"{col}_missing"] = df[col].isna()

            # ---------------------------------------------------------
            # 2. Categorical strategies
            # ---------------------------------------------------------
            if strategy in ["unknown", "none"]:
                if not col_is_categorical:
                    raise ValueError(
                        f"Column '{col}' is numeric but strategy '{strategy}' "
                        "is for categorical variables only."
                    )
                fill_value = "Unknown" if strategy == "unknown" else "None"
                df[col] = df[col].fillna(fill_value)
                continue

            if strategy == "most_frequent":
                if not col_is_categorical:
                    raise ValueError(
                        f"'most_frequent' strategy is only valid for categorical columns. "
                        f"Column '{col}' is numeric."
                    )
                df[col] = df[col].fillna(df[col].mode().iloc[0])
                continue

            # ---------------------------------------------------------
            # 3. Numeric strategies
            # ---------------------------------------------------------
            if strategy == "median":
                if not col_is_numeric:
                    raise ValueError(
                        f"'median' strategy is only valid for numeric columns. "
                        f"Column '{col}' is categorical."
                    )
                df[col] = df[col].fillna(df[col].median())
                continue

            if strategy == "mean":
                if not col_is_numeric:
                    raise ValueError(
                        f"'mean' strategy is only valid for numeric columns. "
                        f"Column '{col}' is categorical."
                    )
                df[col] = df[col].fillna(df[col].mean())
                continue

            # ---------------------------------------------------------
            # 4. Invalid strategy
            # ---------------------------------------------------------
            raise ValueError(
                f"Invalid missing strategy '{strategy}' for column '{col}'."
            )

        return df

    # ---------------------------------------------------------
    # Binning helpers
    # ---------------------------------------------------------
    def _bin_glucose(self, s):
        """ADA 2025 diagnostic cutoffs."""
        bins = [-np.inf, 70, 100, 126, np.inf]
        labels = ["low", "normal", "prediabetic", "diabetic"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_pregnancies(self, s):
        """Parity categories from obstetric epidemiology."""
        bins = [-np.inf, 0.5, 1.5, 5.5, 9.5, np.inf]
        labels = [
            "nulliparous",
            "uniparous",
            "multiparous",
            "grand_multiparous",
            "great_grand_multiparous",
        ]
        return pd.cut(pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels)

    def _bin_blood_pressure(self, s):
        """ACC/AHA diastolic BP categories."""
        bins = [-np.inf, 80, 90, np.inf]
        labels = ["normal_or_elevated", "stage1_htn", "stage2_htn"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_bmi(self, s):
        """WHO BMI categories."""
        bins = [-np.inf, 18.5, 25.0, 30.0, np.inf]
        labels = ["underweight", "normal", "overweight", "obese"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_age(self, s):
        """Epidemiologic age bands."""
        bins = [-np.inf, 40, 60, np.inf]
        labels = ["young_adult", "middle_aged", "older_adult"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_skin(self, s):
        """Cohort-relative adiposity bins."""
        bins = [-np.inf, self.skin_p25_, self.skin_p75_, np.inf]
        labels = ["low_adiposity", "typical_adiposity", "high_adiposity"]
        return pd.cut(pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels)

    def _bin_insulin(self, s):
        """Cohort-relative insulin bins."""
        bins = [-np.inf, self.insulin_p25_, self.insulin_p75_, np.inf]
        labels = ["low_insulin", "typical_insulin", "high_insulin"]
        return pd.cut(pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels)

    def _add_binning(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add feature binning using learned thresholds.
        Assumes missing handling and percentile learning have already occurred.
        """
        df = df.copy()

        if "glucose" in df:
            df["glucose_bin"] = self._bin_glucose(df["glucose"])

        if "pregnancies" in df:
            df["pregnancies_bin"] = self._bin_pregnancies(df["pregnancies"])

        if "blood_pressure" in df:
            df["blood_pressure_bin"] = self._bin_blood_pressure(df["blood_pressure"])

        if "bmi" in df:
            df["bmi_bin"] = self._bin_bmi(df["bmi"])

        if "age" in df:
            df["age_bin"] = self._bin_age(df["age"])

        # Percentile-dependent bins (fit-time learned)
        if "skin_thickness" in df and self.skin_p25_ is not None:
            df["skin_thickness_bin"] = self._bin_skin(df["skin_thickness"])

        if "insulin" in df and self.insulin_p25_ is not None:
            df["insulin_bin"] = self._bin_insulin(df["insulin"])

        return df

    # ---------------------------------------------------------
    # Interaction terms
    # ---------------------------------------------------------
    def _add_interactions(self, df):
        """Create clinically meaningful numeric × numeric interactions."""
        df = df.copy()

        def num(col):
            return pd.to_numeric(df[col], errors="coerce")

        if "glucose" in df and "bmi" in df:
            df["glucose_x_bmi"] = num("glucose") * num("bmi")

        if "insulin" in df and "skin_thickness" in df:
            df["insulin_x_skin_thickness"] = num("insulin") * num("skin_thickness")

        if "age" in df and "diabetes_pedigree_function" in df:
            df["age_x_dpf"] = num("age") * num("diabetes_pedigree_function")

        if "pregnancies" in df and "glucose" in df:
            df["pregnancies_x_glucose"] = num("pregnancies") * num("glucose")

        if "pregnancies" in df and "bmi" in df:
            df["pregnancies_x_bmi"] = num("pregnancies") * num("bmi")

        if "pregnancies" in df and "age" in df:
            df["pregnancies_x_age"] = num("pregnancies") * num("age")

        return df

    # ---------------------------------------------------------
    # Fit
    # ---------------------------------------------------------
    def fit(self, X, y=None):
        """
        Learn cohort percentiles for skin_thickness and insulin.
        Also locks the final output schema.
        """
        df = X.copy()

        # Learned during fit()
        self.skin_p25_ = None
        self.skin_p75_ = None
        self.insulin_p25_ = None
        self.insulin_p75_ = None
        self.feature_names_out_ = []

        # Use default column mapping if not provided
        if self.col_map is None:
            self.col_map = DEFAULT_COL_MAP

        # Apply missing handling
        df = self._handle_missing(df)

        # Learn percentiles
        if "skin_thickness" in df:
            s = pd.to_numeric(df["skin_thickness"], errors="coerce")
            self.skin_p25_, self.skin_p75_ = (
                float(s.quantile(0.25)),
                float(s.quantile(0.75)),
            )

        if "insulin" in df:
            s = pd.to_numeric(df["insulin"], errors="coerce")
            self.insulin_p25_, self.insulin_p75_ = (
                float(s.quantile(0.25)),
                float(s.quantile(0.75)),
            )

        # Drop unwanted columns - drops raw columns. preserves missiingness flag from _handle_missing
        df = df.drop(columns=[c for c in (self.drop_cols or []) if c in df])

        # Lock schema
        df_full = self.transform(df)
        self.feature_names_out_ = list(df_full.columns)

        return self

    # ---------------------------------------------------------
    # Transform
    # ---------------------------------------------------------
    def transform(self, X):
        """
        Apply missing handling, binning, and interactions.
        Enforce schema consistency.
        """
        df = X.copy()

        # Missing handling
        df = self._handle_missing(df)

        # Binning
        if self.create_bins:
            df = self._add_binning(df)

        # Interactions
        if self.create_interactions:
            df = self._add_interactions(df)

        # Drop unwanted columns
        df = df.drop(columns=[c for c in (self.drop_cols or []) if c in df])

        # Schema enforcement
        if self.feature_names_out_:
            for col in self.feature_names_out_:
                if col not in df:
                    df[col] = np.nan
            df = df[self.feature_names_out_]

        return df

    def get_feature_names_out(self, input_features=None):
        """Return final output schema."""
        return np.array(self.feature_names_out_)

    def set_output(self, *, transform: Optional[str] = None):
        """Set output container format."""
        return self


class FeatureCreationEda(BaseEstimator, TransformerMixin):
    """
    EDA-only feature creation for the Pima Indians Diabetes dataset.

    Characteristics:
    - No imputation (zeros preserved except for missingness flags)
    - No interactions
    - No schema locking
    - Only:
        * Missingness exposure
        * Clinical binning
        * Cohort-relative binning for insulin & skinfold thickness
    """

    def __init__(self):
        # learned during fit
        self.skin_p25_ = None
        self.skin_p75_ = None
        self.insulin_p25_ = None
        self.insulin_p75_ = None

    # ---------------------------------------------------------
    # Fit: learn cohort percentiles for skinfold & insulin
    # ---------------------------------------------------------
    def fit(self, X: pd.DataFrame, y=None):
        df = X.copy()

        if "skin_thickness" in df:
            s = pd.to_numeric(df["skin_thickness"], errors="coerce")
            self.skin_p25_ = float(s.quantile(0.25))
            self.skin_p75_ = float(s.quantile(0.75))

        if "insulin" in df:
            s = pd.to_numeric(df["insulin"], errors="coerce")
            self.insulin_p25_ = float(s.quantile(0.25))
            self.insulin_p75_ = float(s.quantile(0.75))

        return self

    # ---------------------------------------------------------
    # Binning helpers (same clinical logic as modeling version)
    # ---------------------------------------------------------
    def _bin_glucose(self, s):
        bins = [-np.inf, 70, 100, 126, np.inf]
        labels = ["low", "normal", "prediabetic", "diabetic"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_pregnancies(self, s):
        bins = [-np.inf, 0.5, 1.5, 5.5, 9.5, np.inf]
        labels = [
            "nulliparous",
            "uniparous",
            "multiparous",
            "grand_multiparous",
            "great_grand_multiparous",
        ]
        return pd.cut(pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels)

    def _bin_blood_pressure(self, s):
        bins = [-np.inf, 80, 90, np.inf]
        labels = ["normal_or_elevated", "stage1_htn", "stage2_htn"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_bmi(self, s):
        bins = [-np.inf, 18.5, 25.0, 30.0, np.inf]
        labels = ["underweight", "normal", "overweight", "obese"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_age(self, s):
        bins = [-np.inf, 40, 60, np.inf]
        labels = ["young_adult", "middle_aged", "older_adult"]
        return pd.cut(
            pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels, right=False
        )

    def _bin_skin(self, s):
        bins = [-np.inf, self.skin_p25_, self.skin_p75_, np.inf]
        labels = ["low_adiposity", "typical_adiposity", "high_adiposity"]
        return pd.cut(pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels)

    def _bin_insulin(self, s):
        bins = [-np.inf, self.insulin_p25_, self.insulin_p75_, np.inf]
        labels = ["low_insulin", "typical_insulin", "high_insulin"]
        return pd.cut(pd.to_numeric(s, errors="coerce"), bins=bins, labels=labels)

    # ---------------------------------------------------------
    # Transform: missingness exposure + binning
    # ---------------------------------------------------------
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()

        # -----------------------------
        # 1. Expose missingness (EDA only)
        # -----------------------------
        for col in ["glucose", "blood_pressure", "skin_thickness", "insulin", "bmi"]:
            if col in df:
                df[f"{col}_missing"] = df[col].isna() | (df[col] == 0)

        # -----------------------------
        # 2. Clinical binning
        # -----------------------------
        if "glucose" in df:
            df["glucose_bin"] = self._bin_glucose(df["glucose"])

        if "pregnancies" in df:
            df["pregnancies_bin"] = self._bin_pregnancies(df["pregnancies"])

        if "blood_pressure" in df:
            df["blood_pressure_bin"] = self._bin_blood_pressure(df["blood_pressure"])

        if "bmi" in df:
            df["bmi_bin"] = self._bin_bmi(df["bmi"])

        if "age" in df:
            df["age_bin"] = self._bin_age(df["age"])

        if "skin_thickness" in df and self.skin_p25_ is not None:
            df["skin_thickness_bin"] = self._bin_skin(df["skin_thickness"])

        if "insulin" in df and self.insulin_p25_ is not None:
            df["insulin_bin"] = self._bin_insulin(df["insulin"])

        return df
