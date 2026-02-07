from typing import Dict

# Default missing handling map (column → imputation strategy)
DEFAULT_COL_MAP: Dict[str, str] = {
    # -----------------------------
    # CATEGORICAL FEATURES
    # -----------------------------

    # (None in this dataset — all features are numeric)

    # -----------------------------
    # NUMERIC FEATURES
    # -----------------------------
    # Glucose is strongly right‑skewed (median 117, max 199).
    # Median is robust to hyperglycemic outliers and preserves clinical central tendency.
    "glucose": "median",
    # Blood pressure is approximately symmetric (mean ≈ 69, median ≈ 72).
    # Mean imputation preserves the population average and is statistically stable.
    "blood_pressure": "mean",
    # Skin thickness is highly skewed with many zeros (missing) and extreme values (up to 99 mm).
    # Median avoids distortion from obesity‑related outliers and noisy measurements.
    "skin_thickness": "median",
    # Insulin is extremely skewed (median 30.5, max 846).
    # Median is the only safe choice — mean would be dominated by extreme insulin resistance cases.
    "insulin": "median",
    # BMI is moderately skewed (median 32, max 67.1).
    # Median avoids overweight/obese outliers pulling the mean upward.
    "bmi": "median",
}
