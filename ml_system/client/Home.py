import streamlit as st
from utils.api import api_client
from utils.ui_components import display_header, display_sidebar_info, render_footer

# Page Config
st.set_page_config(
    page_title="Diabetes Risk AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
display_sidebar_info()

# Main Content
display_header("Diabetes Risk Prediction System", "Advanced AI-Powered Clinical Decision Support")

# System Status Check
with st.spinner("Checking System Health..."):
    is_healthy = api_client.health_check()

if is_healthy:
    st.success("✅ System Operational")
else:
    st.error("❌ System Offline or Unreachable. Please check connection.")
    st.stop()

# Dashboard Overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Welcome
    This system utilizes advanced machine learning algorithms to assess the risk of Type 2 Diabetes based on clinical indicators.
    
    **Key Features:**
    - 📊 **Real-time Risk Prediction**: Instant probability assessment.
    - 🧠 **Explainable AI (XAI)**: Understand *why* a prediction was made using SHAP values.
    - 📉 **Visualization**: Interactive plots for patient data analysis.
    
    ### How to Use
    1. Navigate to **Risk Prediction** to enter patient data.
    2. View the prediction and probability.
    3. Use **Model Explanation** for deeper insights into risk factors.
    """)

    st.info("ℹ️ Select a module from the sidebar to begin.")

with col2:
    st.markdown("### Quick Stats")
    st.metric("Model", "XGBoost Classifier")
    st.metric("Precision", "0.90+ (Clinical Grade)")
    st.metric("Status", "Production")
    
    st.divider()
    st.link_button("🌐 Explore API Documentation", api_client.get_docs_url(), use_container_width=True, help="Open Swagger/OpenAPI documentation")

render_footer()
