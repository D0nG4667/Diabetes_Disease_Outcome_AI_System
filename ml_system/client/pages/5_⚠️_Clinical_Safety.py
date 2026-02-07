import streamlit as st
from utils.ui_components import display_header, display_sidebar_info, render_footer

st.set_page_config(page_title="Clinical Safety", page_icon="⚠️", layout="wide")
display_sidebar_info()
display_header("Clinical Safety & Disclaimers", "Crucial guidelines for safe usage")

st.error("### 🚑 Emergency Warning")
st.markdown("**Do not use this tool for medical emergencies.** If a patient presents with acute symptoms (e.g., ketoacidosis, severe hyperglycemia), follow standard emergency protocols immediately.")

st.divider()

st.markdown("### ⚠️ General Disclaimers")
st.info("""
1. **Adjunct Tool Only:** This AI system is designed to **assist** clinical judgment, not replace it.
2. **Human-in-the-Loop:** All predictions must be verified by a qualified healthcare professional.
3. **No Diagnosis:** This tool provides a *risk probability*, not a definitive medical diagnosis.
""")

st.markdown("### 📉 Known Limitations & Failure Modes")
with st.expander("Read detailed limitations"):
    st.markdown("""
    - **Demographic Bias:** Testing has been limited to specific cohorts. Performance on other ethnicities is not guaranteed.
    - **Outliers:** Extreme values (e.g., BMI > 60, Glucose > 300) may yield unreliable predictions.
    - **Missing Data:** The model generally handles missing values via imputation, but complete data is always preferred for accuracy.
    """)

st.markdown("### 📋 Protocol for High Risk Predictions")
st.markdown("""
- [ ] Verify input data accuracy.
- [ ] Correlate with patient history and physical exam.
- [ ] Order confirmatory lab tests (HbA1c, FPG).
- [ ] initiate standard lifestyle or pharmacological interventions as per guidelines.
""")

render_footer()
