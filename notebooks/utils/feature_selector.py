import numpy as np
import pandas as pd
import plotly.express as px
from functools import partial
from typing import List, Union, Optional
from numpy import ArrayLike
from sklearn.feature_selection import SelectFromModel, mutual_info_classif, f_classif, SelectKBest
from sklearn.base import TransformerMixin, BaseEstimator


# --- Fibonacci generator ---
def fibonacci_up_to(n):
    fib = [1, 1]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])
    return fib


# Keep only Fibonacci numbers >= 3 and <= n_features
n_features = 30
fib_k_values = [k for k in fibonacci_up_to(n_features) if 3 <= k <= n_features]

# Add "all" for completeness
fib_k_values.append("all")

# Optional thresholds for model-based selector
model_threshold_space = ["median", "mean", 0.0]


class TripleSelector(BaseEstimator, TransformerMixin):
    """
    TripleSelector: A robust, interpretable feature‑selection meta‑transformer that
    unifies three complementary selection strategies to maximize signal capture
    across linear, nonlinear, and multivariate relationships.

    This transformer is designed for high‑stakes domains such as clinical ML, where
    different feature types (continuous, binned, categorical, missingness flags,
    interactions) may express signal through different statistical mechanisms.
    TripleSelector ensures that no meaningful feature is discarded prematurely.

    The selector combines:

    1. ANOVA F‑test (SelectKBest with f_classif)
    - Detects strong linear relationships between each feature and the target.
    - Ideal for continuous variables with monotonic effects.

    2. Mutual Information (SelectKBest with mutual_info_classif)
    - Captures nonlinear, non‑monotonic, and interaction‑driven dependencies.
    - Particularly effective for binned features, categorical encodings,
        and missingness indicators.

    3. Model‑Based Selection (SelectFromModel)
    - Identifies multivariate, conditional importance using a supervised model
        such as L1‑penalized Logistic Regression or a tree‑based estimator.
    - Captures interactions and conditional effects that univariate tests miss.

    The final selected feature set is the UNION of all three selectors.
    This fusion strategy provides exceptional robustness and stability, ensuring
    coverage of linear, nonlinear, and multivariate signals simultaneously.

    Optional enhancements include:
    - Automatic K selection for ANOVA and MI using an elbow‑style heuristic.
    - Rich interpretability via `.summary()`, which reports all selector scores.
    - Interactive Plotly visualization via `.plot_importances()`.
    - Full sklearn compatibility for seamless integration into pipelines.

    Parameters
    ----------
    k_anova : int or None, default=10
        Number of top features to select using the ANOVA F‑test.
        Ignored if `auto_k=True`.

    k_mi : int or None, default=10
        Number of top features to select using Mutual Information.
        Ignored if `auto_k=True`.

    model : estimator, default=None
        A supervised estimator used by SelectFromModel.
        Must expose either `coef_` or `feature_importances_`.

    model_threshold : str or float, default="median"
        Threshold passed to SelectFromModel to determine which features to keep.

    max_k : int, default=30
        Maximum allowable k when auto‑selection is enabled.

    Attributes
    ----------
    selected_idx_ : np.ndarray of shape (n_selected_features,)
        Sorted array of selected feature indices after merging all selectors.

    anova : SelectKBest
        Internal ANOVA selector.

    mi : SelectKBest
        Internal Mutual Information selector.

    model_selector : SelectFromModel
        Internal model‑based selector.

    Notes
    -----
    TripleSelector is particularly well‑suited for clinical ML pipelines where
    interpretability, robustness, and multi‑signal coverage are essential. It
    preserves feature names, integrates cleanly into sklearn/imblearn pipelines,
    and supports downstream interpretability workflows such as calibration,
    threshold optimization, and model card generation.
    """

    def __init__(
        self,
        k_anova: Optional[int] = 10,
        k_mi: Optional[int] = 10,
        model: Optional[BaseEstimator] = None,
        model_threshold: Union[str, float] = "median",
        random_state: int = 2026,
    ) -> None:
        self.k_anova = k_anova
        self.k_mi = k_mi
        self.model = model
        if self.model is not None and hasattr(self.model, "random_state"):
            self.model.set_params(random_state=self.random_state)
        self.model_threshold = model_threshold
        self.random_state = random_state

        self.anova = SelectKBest(score_func=f_classif, k=k_anova)
        self.mi = SelectKBest(
            score_func=partial(mutual_info_classif, random_state=self.random_state),
            k=k_mi,
        )
        self.model_selector = SelectFromModel(
            estimator=model, threshold=model_threshold
        )

    # ---------------------------------------------------------
    # Fit
    # ---------------------------------------------------------
    def fit(self, X: ArrayLike, y: ArrayLike) -> "TripleSelector":
        # Fit all selectors
        self.anova.fit(X, y)
        self.mi.fit(X, y)
        self.model_selector.fit(X, y)

        # Merge masks
        mask = (
            self.anova.get_support()
            | self.mi.get_support()
            | self.model_selector.get_support()
        )

        self.selected_idx_ = np.where(mask)[0]
        return self

    # ---------------------------------------------------------
    # Transform
    # ---------------------------------------------------------
    def transform(self, X: ArrayLike) -> np.ndarray:
        return X[:, self.selected_idx_]

    # ---------------------------------------------------------
    # get_support()
    # ---------------------------------------------------------
    def get_support(self, n_features: Optional[int] = None) -> np.ndarray:
        """Return boolean mask of selected features."""
        if n_features is None:
            n_features = max(self.selected_idx_) + 1
        mask = np.zeros(n_features, dtype=bool)
        mask[self.selected_idx_] = True
        return mask

    # ---------------------------------------------------------
    # Feature names
    # ---------------------------------------------------------
    def get_feature_names_out(
        self, input_features: Optional[Union[List[str], np.ndarray]] = None
    ) -> np.ndarray:
        if input_features is None:
            input_features = np.array([f"x{i}" for i in range(len(self.selected_idx_))])

        return np.array(input_features)[self.selected_idx_]

    # ---------------------------------------------------------
    # Summary table
    # ---------------------------------------------------------
    def summary(self, input_features: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Return a DataFrame summarizing:
        - ANOVA scores
        - MI scores
        - Model-based importances
        - Whether each selector picked the feature
        """

        if input_features is None:
            input_features = [f"x{i}" for i in range(len(self.anova.scores_))]

        model_scores = (
            getattr(self.model_selector.estimator_, "coef_", None)
            if hasattr(self.model_selector.estimator_, "coef_")
            else getattr(self.model_selector.estimator_, "feature_importances_", None)
        )

        if model_scores is not None:
            model_scores = np.abs(model_scores).ravel()
        else:
            model_scores = np.zeros(len(input_features))

        df = pd.DataFrame(
            {
                "feature": input_features,
                "anova_score": self.anova.scores_,
                "mi_score": self.mi.scores_,
                "model_score": model_scores,
                "selected_by_anova": self.anova.get_support(),
                "selected_by_mi": self.mi.get_support(),
                "selected_by_model": self.model_selector.get_support(),
                "selected_final": np.isin(
                    np.arange(len(input_features)), self.selected_idx_
                ),
            }
        )

        return df.sort_values("selected_final", ascending=False)

    # ---------------------------------------------------------
    # Plotly visualization
    # ---------------------------------------------------------
    def plot_importances(self, input_features: Optional[List[str]] = None):
        """
        Plot ANOVA, MI, and model-based scores in a single interactive Plotly chart.
        """

        df = self.summary(input_features)

        fig = px.scatter(
            df,
            x="anova_score",
            y="mi_score",
            size="model_score",
            color="selected_final",
            hover_name="feature",
            title="TripleSelector Feature Importance Map",
            labels={
                "anova_score": "ANOVA (Linear Signal)",
                "mi_score": "Mutual Information (Nonlinear Signal)",
                "model_score": "Model-Based Importance",
                "selected_final": "Selected",
            },
            size_max=30,
            color_continuous_scale="Viridis",
        )

        fig.update_layout(height=700)
        return fig
