import streamlit as st
import base64
from utils.api import api_client
from utils.ui_components import display_header, display_sidebar_info, render_footer, render_feature_input_section

st.set_page_config(page_title="Model Explanation", page_icon="🧠", layout="wide")
display_sidebar_info()
display_header("Model Explanation (XAI)", "Interpret prediction results using SHAP")

# Navigation helper
col_nav, _ = st.columns([1, 4])
with col_nav:
    if st.button("⬅️ Back to Prediction", use_container_width=True):
        st.switch_page("pages/1_📊_Risk_Prediction.py")

# Check if we have patient data
if "patient_data" not in st.session_state:
    st.warning("⚠️ No patient data found. Please go to **Risk Prediction** and perform a prediction first.")
    st.stop()

# Allow editing
with st.expander("📝 Edit Patient Data", expanded=False):
    st.info("💡 Modify values below to simulate 'What-if' scenarios.")
    st.session_state.patient_data = render_feature_input_section(defaults=st.session_state.patient_data)

st.info("💡 Explanations visualize which features pushed the risk score higher (Positive) or lower (Negative).")

col1, col2 = st.columns([1, 1])
with col1:
    top_n = st.slider("Number of Top Features", 5, 20, 10, help="Select number of most important features to display")
with col2:
    plot_toggle = st.checkbox("Generate Summary Plot", value=True, help="Generate visual SHAP summary plot")

if st.button("Generate Explanation", type="primary"):
    with st.spinner("Computing SHAP values (this may take a moment)..."):
        # API call
        explanation = api_client.explain(st.session_state.patient_data, top_n=top_n, plot=plot_toggle)

    if explanation:
        st.subheader("Top Contributing Features")
        
        # Parse features
        features = explanation.get("top_features", [])
        
        # Display as chart
        if features:
            import plotly.graph_objects as go

            # --- Chart 1: Horizontal Bar Chart (Feature Importance) ---
            feature_names = [f["feature"] for f in features]
            shap_values = [f["value"] for f in features]
            
            # Sort for display (Top feature at top)
            feature_names = feature_names[::-1]
            shap_values = shap_values[::-1]
            
            # Color Logic: Red (Risk) vs Green (Protective)
            colors = ['#ef4444' if v > 0 else '#10b981' for v in shap_values]
            
            fig_bar = go.Figure(go.Bar(
                x=shap_values,
                y=feature_names,
                orientation='h',
                marker_color=colors,
                texttemplate="%{x:.3f}",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Impact: %{x:.4f}<extra></extra>"
            ))
            
            fig_bar.update_layout(
                title="Top Contributing Features (Red=Risk, Green=Protective)",
                xaxis_title="SHAP Value (Impact on Prediction)",
                yaxis_title="Feature",
                height=400 + (len(features) * 20),
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_bar, width='stretch')

            # --- Clinical Interpretation ---
            st.markdown("### Clinical Interpretation")
            # Iterate original order (descending importance)
            for f in features[:3]: 
                impact = "increased" if f["value"] > 0 else "decreased"
                color = "red" if f["value"] > 0 else "green"
                st.markdown(f"- **{f['feature']}** :{color}[{impact}] the risk score (Impact: {f['value']:.4f})")

            # --- Chart 2: Summary Plot (Server-side Generated) ---
            if plot_toggle and explanation.get("shap_plot_base64"):
                st.divider()
                st.subheader("Feature Impact Distribution")
                try:
                    # Decode base64 header if present, though API likely sends raw b64 or data uri
                    b64_str = explanation["shap_plot_base64"]
                    if "," in b64_str:
                        b64_str = b64_str.split(",")[1]
                    
                    image_bytes = base64.b64decode(b64_str)
                    st.image(image_bytes, caption="SHAP Summary Plot (Global Context)", width="stretch")
                except Exception as e:
                    st.error(f"Failed to render plot: {e}")

render_footer()
