import streamlit as st
import pandas as pd
from utils.ui_components import (
    load_css, render_header, render_sidebar_info, 
    render_feature_input_section, render_prediction_result, card, render_footer
)
from utils.api import api_client

st.set_page_config(page_title="Risk Prediction", page_icon="📊", layout="wide")
load_css()

render_header("📊 Deep Learning Risk Prediction", "Assess Patient Diabetes Risk")

tab1, tab2 = st.tabs(["👤 Single Patient", "📂 Batch Processing"])

# --- Single Prediction ---
with tab1:
    # Inputs (Full Width)
    defaults = st.session_state.get("patient_data", {})
    inputs = render_feature_input_section(defaults=defaults)
    
    # Action & Results
    col_action, col_res = st.columns([1, 2])
    with col_action:
        predict_btn = st.button("🩺 Predict Risk", type="primary", width="stretch")
        
        # Sync Toast (Only show if NOT about to predict)
        if defaults and not predict_btn:
             st.toast("Patient vitals synced from session", icon="🔄")
        
        # Placeholder for explanation button (appears under predict button)
        explain_placeholder = st.empty()
    
    with col_res:
        if predict_btn:
            with st.spinner("Running Deep Learning Inference..."):
                result = api_client.predict(inputs)
            
            if result:
                st.toast("Prediction complete!", icon="✅")
                # Display Key Result
                render_prediction_result(result["probability"], result["threshold"])
                
                # Metadata / Debug
                with st.expander("ℹ️ Model Metadata"):
                    st.json(result.get("metadata", {}))
                
                # Store in session state
                st.session_state["patient_data"] = inputs
                st.session_state["last_result"] = result
        
        elif "last_result" in st.session_state:
             st.info("Last prediction result is cached.")
             # Render result from cache if needed, or just leave info.
             # Actually, if cached, we might want to show the result card again?
             # For now, just keeping the info message as per prev logic, but moving button.
             result = st.session_state["last_result"]
             render_prediction_result(result["probability"], result["threshold"])

    # Render Explanation Button in the left column if result exists
    if "last_result" in st.session_state:
        with explain_placeholder:
            if st.button("👉 View Model Explanation", width="stretch"):
                st.switch_page("pages/2_🧠_Model_Explanation.py")

# --- Batch Prediction ---
with tab2:
    st.markdown("### 📂 Batch Patient Processing")
    
    col_info, col_dl = st.columns([3, 1])
    with col_info:
        st.info("Upload a CSV file containing patient data. The file must contain the required clinical columns.")
    
    with col_dl:
        # Template Download
        template_data = {
            "pregnancies": [1, 3],
            "glucose": [85, 140],
            "blood_pressure": [66, 80],
            "skin_thickness": [29, 35],
            "insulin": [0, 160],
            "bmi": [26.6, 32.0],
            "diabetes_pedigree_function": [0.351, 0.5],
            "age": [31, 50]
        }
        df_template = pd.DataFrame(template_data)
        csv_template = df_template.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Template", csv_template, "patient_batch_template.csv", "text/csv", width="stretch")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            
            # Sanity Check
            required_columns = {
                "pregnancies", "glucose", "blood_pressure", "skin_thickness", 
                "insulin", "bmi", "diabetes_pedigree_function", "age"
            }
            
            # Normalize columns to lowercase for check
            df_cols = set(col.lower() for col in df_upload.columns)
            missing = required_columns - df_cols
            
            if missing:
                st.error(f"❌ Missing required columns: {', '.join(missing)}")
                st.stop()
            else:
                # Avoid showing toast on every rerun
                file_id = f"{uploaded_file.name}-{uploaded_file.size}"
                if st.session_state.get("validated_file_id") != file_id:
                    st.toast("✅ CSV File Validated!", icon="✅")
                    st.session_state["validated_file_id"] = file_id
            
            with st.expander("👀 Preview Data", expanded=True):
                st.dataframe(df_upload.head(), width="stretch")
            
            if st.button("⚙️ Process Batch", type="primary"):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_rows = len(df_upload)
                success_count = 0
                
                for index, row in df_upload.iterrows():
                    # Build payload from row (handling potential case sensitivity map if needed)
                    # Using clean mapping ensuring strictly correct types for API
                    try:
                        payload = {
                            "pregnancies": int(row.get("pregnancies", row.get("Pregnancies", 0))),
                            "glucose": float(row.get("glucose", row.get("Glucose", 0))),
                            "blood_pressure": float(row.get("blood_pressure", row.get("BloodPressure", 0))),
                            "skin_thickness": float(row.get("skin_thickness", row.get("SkinThickness", 0))),
                            "insulin": float(row.get("insulin", row.get("Insulin", 0))),
                            "bmi": float(row.get("bmi", row.get("BMI", 0))),
                            "diabetes_pedigree_function": float(row.get("diabetes_pedigree_function", row.get("DiabetesPedigreeFunction", 0))),
                            "age": int(row.get("age", row.get("Age", 0)))
                        }
                        
                        api_res = api_client.predict(payload)
                        
                        if api_res:
                            results.append({
                                **payload,
                                "Risk_Probability": api_res["probability"],
                                "Prediction": "High Risk" if api_res["outcome"] == 1 else "Low Risk",
                                "Threshold": api_res["threshold"]
                            })
                            success_count += 1
                        else:
                            results.append({
                                **payload,
                                "Risk_Probability": None,
                                "Prediction": "API Error",
                                "Threshold": None
                            })
                    except Exception as e:
                         results.append({
                            **row.to_dict(),
                            "Risk_Probability": None,
                            "Prediction": f"Data Error: {str(e)}",
                            "Threshold": None
                        })

                    # Update progress
                    progress = (index + 1) / total_rows
                    progress_bar.progress(progress)
                    status_text.text(f"Processing row {index + 1}/{total_rows}")
                
                status_text.empty()
                st.toast(f"Processing complete! ({success_count}/{total_rows} successful)", icon="🎉")
                
                # Show results DF
                result_df = pd.DataFrame(results)
                
                # Summary Metrics
                high_risk_count = len(result_df[result_df["Prediction"] == "High Risk"])
                low_risk_count = len(result_df[result_df["Prediction"] == "Low Risk"])
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Patients", total_rows)
                c2.metric("High Risk Detected", high_risk_count, delta_color="inverse")
                c3.metric("Low Risk Detected", low_risk_count)

                st.dataframe(result_df, width="stretch")
                
                # Download
                csv_results = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Results CSV",
                    csv_results,
                    "batch_predictions.csv",
                    "text/csv",
                    type="primary"
                )
                
        except Exception as e:
            st.error(f"Error processing file: {e}")

render_sidebar_info()
render_footer()
