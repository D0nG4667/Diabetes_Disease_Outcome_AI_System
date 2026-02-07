import streamlit as st
from pathlib import Path
from utils.api import api_client

def load_css():
    """Inject CSS into Streamlit app from assets/css/style.css."""
    # Resolve path relative to this file: utils/ui_components.py -> utils -> client -> assets...
    css_path = Path(__file__).resolve().parent.parent / "assets" / "css" / "style.css"
    
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found at: {css_path}")
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

def render_header(title: str, subtitle: str = ""):
    """Render a styled header."""
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"### {subtitle}")
    st.markdown("---")

def render_sidebar_info():
    """Render common sidebar info with dynamic status."""
    status = api_client.get_detailed_status()
    
    # Icons
    icon_conn = "🟢" if status["connection"] else "🔴"
    icon_auth = "🔑" if status["auth"] else "🔒"
    icon_model = "🧠" if status["model"] else "💤"
    
    st.sidebar.info(
        f"""
        **System Status**
        
        {icon_conn} Connectivity: {"Online" if status["connection"] else "Offline"}  
        {icon_auth} Auth: {"Valid" if status["auth"] else "Invalid"}  
        {icon_model} Model: {"Ready" if status["model"] else "Not Ready"}
        
        _{status["message"]}_
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(f"v1.0.0 | © 2026 HealthAI System")

def card(content: str, title: str = None):
    """Render a content card."""
    if title:
        st.markdown(f"### {title}")
    st.markdown(
        f"""
        <div class="css-card">
        {content}
        </div>
        """,
        unsafe_allow_html=True
    )

def render_prediction_result(prob: float, threshold: float):
    """Render formatted prediction result."""
    is_high_risk = prob >= threshold
    
    color_class = "risk-high" if is_high_risk else "risk-low"
    outcome_text = "HIGH RISK (Positive)" if is_high_risk else "LOW RISK (Negative)"
    emoji = "⚠️" if is_high_risk else "✅"
    
    progress_color = "#ef4444" if is_high_risk else "#3b82f6"
    
    st.markdown(
        f"""
        <div class="css-card metric-container {color_class}" style="margin-bottom: 30px;">
            <h2 style="margin:0; color: #333;">{emoji} {outcome_text}</h2>
        </div>
        <style>
            .stProgress > div > div > div > div {{
                background-color: {progress_color};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.progress(prob)
    st.caption(f"Risk Probability: {prob:.1%} (Clinical Threshold: {threshold:.2f})")
    
    # Clinical Recommendations
    if is_high_risk:
        st.markdown(
            """
            <div style="background-color: #fff7ed; padding: 15px; border-left: 5px solid #f97316; border-radius: 4px; margin-top: 15px;">
                <h4 style="margin:0; color: #9a3412;">🩺 Clinical Assessment Protocol</h4>
                <p style="margin-top: 5px; color: #431407; font-size: 0.95rem;">
                    <b>Immediate Diagnostic Action:</b> The estimated risk exceeds the validated clinical threshold. 
                    Correlation with laboratory diagnostics (HbA1c ≥ 6.5% or FPG ≥ 126 mg/dL) is recommended. 
                    Initiate intensive lifestyle modification counseling and screen for associated microvascular complications 
                    consistent with standardized STEPwise protocols.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background-color: #f0f9ff; padding: 15px; border-left: 5px solid #0ea5e9; border-radius: 4px; margin-top: 15px;">
                <h4 style="margin:0; color: #0c4a6e;">🛡️ Proactive Prevention Strategy</h4>
                <p style="margin-top: 5px; color: #082f49; font-size: 0.95rem;">
                    <b>Routine Clinical Monitoring:</b> Risk is currently below the diagnostic threshold. 
                    Maintain primary prevention through evidence-based nutritional patterns and physical activity. 
                    Periodic re-evaluation of clinical status is recommended every 24-36 months or upon 
                    emergence of symptomatic indicators.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<br>", unsafe_allow_html=True)

def render_feature_input_section(defaults: dict = {}):
    """Returns a dictionary of input features matching Pima Indians Diabetes dataset."""
    st.subheader("Patient Vitals")
    
    c1, c2 = st.columns(2)
    
    with c1:
        with st.expander("👤 Demographics & History", expanded=True):
            pregnancies = st.number_input("Pregnancies", 0, 20, int(defaults.get("pregnancies", 1)), step=1, help="Number of times pregnant")
            age = st.number_input("Age (years)", 21, 100, int(defaults.get("age", 33)), step=1, help="Patient age in years")
            diabetes_pedigree_function = st.number_input("Diabetes Pedigree Function", 0.0, 2.5, float(defaults.get("diabetes_pedigree_function", 0.47)), step=0.01, format="%.3f", help="Diabetes pedigree function")

    with c2:
        with st.expander("🧪 Lab Results & Body Metrics", expanded=True):
            glucose = st.number_input("Glucose (mg/dL)", 0, 200, int(defaults.get("glucose", 120)), step=1, help="Plasma glucose concentration")
            blood_pressure = st.number_input("Blood Pressure (mm Hg)", 0, 300, int(defaults.get("blood_pressure", 70)), step=1, help="Diastolic blood pressure")
            skin_thickness = st.number_input("Skin Thickness (mm)", 0, 100, int(defaults.get("skin_thickness", 20)), step=1, help="Triceps skin fold thickness")
            insulin = st.number_input("Insulin (mu U/ml)", 0, 900, int(defaults.get("insulin", 80)), step=1, help="2-Hour serum insulin")
            bmi = st.number_input("BMI", 0.0, 70.0, float(defaults.get("bmi", 32.0)), step=0.1, help="Body Mass Index")
    
    return {
        "pregnancies": pregnancies,
        "glucose": glucose,
        "blood_pressure": blood_pressure,
        "skin_thickness": skin_thickness,
        "insulin": insulin,
        "bmi": bmi,
        "diabetes_pedigree_function": diabetes_pedigree_function,
        "age": age
    }

def render_footer():
    """
    Standard footer.
    """
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            color: #6b7280;
            text-align: center;
            padding: 10px;
            border-top: 1px solid #e5e7eb;
            font-size: 0.8rem;
            z-index: 1000;
        }
        </style>
        <div class="footer">
            © 2026 Healthcare AI Systems.<br>
            Not for direct diagnostic use without clinician review.<br>
            Made with ❤️ by <a href="https://linkedin.com/in/dr-gabriel-okundaye" target="_blank">Dr. Gabriel Okundaye</a>
        </div>
        """,
        unsafe_allow_html=True
    )
