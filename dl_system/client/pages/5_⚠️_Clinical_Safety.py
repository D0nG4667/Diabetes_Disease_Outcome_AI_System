import streamlit as st
from utils.ui_components import load_css, render_header, render_sidebar_info, render_footer

st.set_page_config(page_title="Clinical Safety", page_icon="⚠️", layout="wide")
load_css()

render_header("⚠️ Clinical Safety & Disclaimers", "Important Usage Guidelines")

st.warning("""
### 🚨 EMERGENCY WARNING
**This system is NOT designed for emergency use.**
If a patient is presenting with acute symptoms of Validation (e.g., ketoacidosis, hyperosmolar hyperglycemic state), proceed immediately to standard emergency protocols. Do not wait for model inference.
""")

st.markdown("""
### 🛡️ Human-in-the-Loop Requirement
- **Decision Support Only**: This AI is a decision SUPPORT tool, not a decision MAKER.
- **Clinical Oversight**: All predictions must be reviewed by a qualified healthcare professional.
- **Override Authority**: Clinicians should override model output if it contradicts clinical judgment or patient presentation.

### 🧪 Known Failure Modes
1.  **Out-of-Distribution Data**: Patients significantly older (>80) or younger (<21) than the training set may have unreliable predictions.
2.  **Missing Data**: While the system handles missing values via imputation, excessive missingness (>50% of fields) degrades confidence.
3.  **Rare Comorbidities**: The model does not account for rare genetic disorders affecting glucose metabolism.

### 🌡️ Calibration & Uncertainty
- The model outputs a **probability**, not a certainty. 
- A probability of 0.85 means that out of 100 patients with *identical* features, 85 are expected to have the outcome.
- Temperature scaling has been applied to align probabilities with real-world observed frequencies.

### 🔒 Data Privacy
- This client application is stateless.
- **No PHI (Protected Health Information)** is stored in the browser or persisted on the server by default.
- Ensure you are using a secure network when transmitting patient vitals.
""")

render_sidebar_info()
render_footer()
