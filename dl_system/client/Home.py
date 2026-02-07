import streamlit as st
from pathlib import Path
from utils.ui_components import load_css, render_header, render_sidebar_info, card, render_footer
from utils.api import api_client

# Resolve paths
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logos" / "logo.png"

# Page Config
st.set_page_config(
    page_title="Diabetes Risk AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Styles
load_css()

# Main Content
render_header("🏥 Diabetes Risk AI System", "Deep Learning Clinical Decision Support")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Welcome to the Clinical AI Assistant
    
    This system utilizes advanced Deep Learning models (TensorFlow/Keras) calibrated with temperature scaling to estimate diabetes risk based on patient vitals and history.
    
    **Key Features:**
    - ⚡ **Real-time Risk Prediction**: Instant inference via FastAPI backend.
    - 🧠 **Explainable AI (SHAP)**: Feature importance transparency.
    - 🌡️ **Calibrated Probabilities**: Reliable risk estimates.
    - 🛡️ **Privacy First**: No patient data storage.
    """)
    
    st.info("👈 **Navigate using the sidebar** to access prediction and explanation tools.")

    st.markdown("### Modules")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        card("""
        #### 📊 Risk Prediction
        Input patient data to get immediate risk assessment and calibrated probabilities.
        """, title=None)
    
    with c2:
        card("""
        #### 🧠 Interpretability
        Understand *why* a prediction was made using SHAP values and feature contribution plots.
        """, title=None)

    with c3:
        status = api_client.get_detailed_status()
        status_icon = "✅" if status["healthy"] else "❌"
        status_text = "Operational" if status["healthy"] else "Issues Detected"
        
        card(f"""
        #### 🖥️ System Health
        **Status**: {status_text} {status_icon}
        
        {status["message"]}
        """, title=None)

with col2:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    else:
        st.info("Clinical Decision Support Tool")
    
    st.warning("""
    **Disclaimer**: This tool is for **investigational use only**. 
    It is not a substitute for professional medical diagnosis. 
    Always verify results with standard clinical protocols.
    """)

render_sidebar_info()
render_footer()
