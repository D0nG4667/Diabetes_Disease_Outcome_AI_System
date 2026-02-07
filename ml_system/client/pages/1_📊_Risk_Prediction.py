import streamlit as st
from utils.api import api_client
from utils.ui_components import display_header, display_sidebar_info, render_footer, render_feature_input_section, render_prediction_result
from datetime import datetime

st.set_page_config(page_title="Risk Prediction", page_icon="📊", layout="wide")

display_sidebar_info()
display_header("Patient Risk Prediction", "Enter clinical parameters for assessment")

import pandas as pd

# Tabs for Mode Selection
tab1, tab2 = st.tabs(["Manual Assessment", "Batch Assessment (CSV)"])

with tab1:
    # Initialize Session State for Patient Data
    if "patient_data" not in st.session_state:
        st.session_state.patient_data = {
            "pregnancies": 0,
            "glucose": 100.0,
            "blood_pressure": 72.0,
            "skin_thickness": 20.0,
            "insulin": 80.0,
            "bmi": 25.0,
            "diabetes_pedigree_function": 0.5,
            "age": 30
        }

    # Input Form
    inputs = render_feature_input_section(defaults=st.session_state.patient_data)
    
    col_btn, col_res = st.columns([1, 2])
    with col_btn:
        submit_btn = st.button("🩺 Predict Risk", type="primary", use_container_width=True)
        explain_placeholder = st.empty()

    with col_res:
        if submit_btn:
            # Update session state with new inputs
            st.session_state.patient_data = inputs

            # Call API
            with st.spinner("Analyzing patient data..."):
                result = api_client.predict(st.session_state.patient_data)

            if result:
                st.toast("Assessment Complete!", icon="🩺")
                # Save result to session state
                st.session_state.last_prediction = result
                
                render_prediction_result(result["probability"], result["threshold"])
        
        elif "last_prediction" in st.session_state:
            result = st.session_state.last_prediction
            render_prediction_result(result["probability"], result["threshold"])

    # Show Explanation Button if we have a result
    if "last_prediction" in st.session_state:
        with explain_placeholder:
            if st.button("👉 View Model Explanation", use_container_width=True):
                st.switch_page("pages/2_🧠_Model_Explanation.py")

with tab2:
    st.markdown("### Batch Prediction Upload")
    st.info("Upload a CSV file containing patient data. The file must contain the required clinical columns.")
    
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
    st.download_button("Download CSV Template", csv_template, "template.csv", "text/csv")
    
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
                # Avoid showing toast on every rerun (e.g. when switching tabs or clicking predict in other tab)
                file_id = f"{uploaded_file.name}-{uploaded_file.size}"
                if st.session_state.get("validated_file_id") != file_id:
                    st.toast("✅ CSV File Validated!", icon="✅")
                    st.session_state["validated_file_id"] = file_id
            
            st.write("Preview:", df_upload.head())
            
            if st.button("Process Batch"):
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_rows = len(df_upload)
                
                for index, row in df_upload.iterrows():
                    # Build payload from row (handling potential case sensitivity map if needed, 
                    # but assuming template adherence for now)
                    payload = {
                        "pregnancies": int(row.get("pregnancies", 0)),
                        "glucose": float(row.get("glucose", 0)),
                        "blood_pressure": float(row.get("blood_pressure", 0)),
                        "skin_thickness": float(row.get("skin_thickness", 0)),
                        "insulin": float(row.get("insulin", 0)),
                        "bmi": float(row.get("bmi", 0)),
                        "diabetes_pedigree_function": float(row.get("diabetes_pedigree_function", 0)),
                        "age": int(row.get("age", 0))
                    }
                    
                    api_res = api_client.predict(payload)
                    
                    if api_res:
                        results.append({
                            **payload,
                            "probability": api_res["probability"],
                            "outcome": api_res["outcome"],
                            "threshold": api_res["threshold"]
                        })
                    else:
                        results.append({
                            **payload,
                            "probability": None,
                            "outcome": "Error",
                            "threshold": None
                        })
                    
                    # Update progress
                    progress = (index + 1) / total_rows
                    progress_bar.progress(progress)
                    status_text.text(f"Processing row {index + 1}/{total_rows}")
                
                status_text.text("Batch processing complete!")
                
                # Show results DF
                df_results = pd.DataFrame(results)
                st.dataframe(df_results)
                
                # Download
                csv_results = df_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Results",
                    csv_results,
                    "batch_predictions.csv",
                    "text/csv",
                    type="primary"
                )
                
        except Exception as e:
            st.error(f"Error processing file: {e}")

render_footer()
