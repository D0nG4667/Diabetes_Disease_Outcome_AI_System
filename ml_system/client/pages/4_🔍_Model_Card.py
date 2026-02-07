import streamlit as st
from utils.ui_components import display_header, display_sidebar_info, render_footer

st.set_page_config(page_title="Model Card", page_icon="🔍", layout="wide")
display_sidebar_info()
display_header("Model Card", "Transparency and performance details")

# Model Details
st.markdown("## Model Details")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Name:** Diabetes Risk XGBoost Classifier")
    st.markdown("**Version:** 1.0.0")
    st.markdown("**Type:** Gradient Boosted Decision Trees (XGBoost)")
    st.markdown("**Date:** 2026-02-05")
with col2:
    st.markdown("**License:** Proprietary / Clinical Research")
    st.markdown("**Frameworks:** Scikit-learn, XGBoost, Imbalanced-learn")
    st.markdown("**Input:** 8 Clinical Features")

st.divider()

# Intended Use
st.markdown("## Intended Use")
st.markdown("""
- **Primary Use:** Decision support tool for clinicians to assess Type 2 Diabetes risk in adults (female cohort based on logic).
- **Intended Users:** Healthcare providers, endocrinologists.
- **Out of Scope:** Automatic diagnosis without human review, pediatric use.
""")

st.divider()

# Performance
st.markdown("## Performance Metrics (Validation Set)")
metrics = {
    "Recall (Sensitivity)": "Production Grade (>=90%) - Optimized for high sensitivity to minimize false negatives.",
    "Precision": "(>=50%) - alert fatigue.",
    "AUC-ROC": "(>=79%) - discriminatory power."
}
st.json(metrics)

st.divider()

# Ethical Considerations
st.markdown("## Ethical Considerations")
st.warning("""
- **Bias:** Training data consists primarily of Pima Indian heritage females. Results may need calibration for other demographics.
- **Fairness:** Model optimized to reduce false negatives to prioritize early intervention.
- **Privacy:** System is stateless; minimal patient PHI is processed (only clinical values).
""")

render_footer()
