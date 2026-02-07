import streamlit as st
import base64
import pandas as pd
from utils.ui_components import (
    load_css, render_header, render_sidebar_info, render_footer,
    render_feature_input_section
)
from utils.api import api_client

st.set_page_config(page_title="Model Explanation", page_icon="🧠", layout="wide")
load_css()

render_header("🧠 DL Model Explanation", "Interpretability via SHAP (SHapley Additive exPlanations)")

# Check session state for inputs
inputs = st.session_state.get("last_prediction", None)

if not inputs:
    st.warning("⚠️ No recent prediction found. Please go to the **Risk Prediction** page to generate a prediction first.")
    if st.button("👉 Go to Risk Prediction"):
        st.switch_page("pages/1_📊_Risk_Prediction.py")
    st.stop()
else:
    st.success("Using data from last prediction.")
    
    # Allow editing
    with st.expander("📝 Edit Patient Data", expanded=False):
        st.info("💡 You can modify values below to simulate 'What-if' scenarios.")
        inputs = render_feature_input_section(defaults=inputs)

# Controls
col_ctrl, _ = st.columns([1, 2])
with col_ctrl:
    top_n = st.slider("Top Features to Display", 5, 20, 10)
    
if st.button("🔍 Run SHAP Analysis", type="primary"):
    # Update session state with potentially edited values
    st.session_state["last_prediction"] = inputs
    
    with st.spinner("Calculating Shapley values using DeepExplainer... (This may take a moment)"):
        # Call API
        explanation = api_client.explain(inputs, top_n=top_n, plot=True)
        
    if explanation:
        st.toast("SHAP analysis complete!", icon="🧠")
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
            


            # Color Logic: Red (Risk) vs Blue (Protective)
            colors = ['#ef4444' if v > 0 else '#3b82f6' for v in shap_values]
            
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
                title="Top Contributing Features (Red=Risk, Blue=Protective)",
                xaxis_title="SHAP Value (Impact on Prediction)",
                yaxis_title="Feature",
                height=400 + (len(features) * 20),
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_bar, width="stretch")

            # --- Clinical Interpretation ---
            st.markdown("### Clinical Interpretation")
            # Iterate original order (descending importance)
            for f in features[:3]: 
                impact = "increased" if f["value"] > 0 else "decreased"
                color = "red" if f["value"] > 0 else "blue"
                st.markdown(f"- **{f['feature']}** :{color}[{impact}] the risk score (Impact: {f['value']:.4f})")

            # --- Chart 2: Summary Plot (Server-side Generated) ---
            if explanation.get("shap_plot_base64"):
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

        st.markdown("---")
        st.markdown("""
        **Clinical Interpretation**:
        SHAP values represent the *impact* of a feature on the model's output probability log-odds.
        - **Red** bars/points generally indicate higher values of the feature pushing the risk HIGHER.
        - **Blue** bars/points indicate values pushing the risk LOWER.
        """)

render_sidebar_info()
render_footer()
