import streamlit as st
from utils.ui_components import display_header, display_sidebar_info, render_footer
import pandas as pd

st.set_page_config(page_title="Data Dictionary", page_icon="📘", layout="wide")
display_sidebar_info()
display_header("Clinical Data Dictionary", "Definitions and normal ranges for input variables")

data = [
    {
        "Variable": "Pregnancies",
        "Description": "Number of times pregnant",
        "Clinical Relevance": "Higher number of pregnancies can be associated with higher risk of gestational diabetes and T2DM later.",
        "Normal Range": "N/A"
    },
    {
        "Variable": "Glucose",
        "Description": "Plasma glucose concentration a 2 hours in an oral glucose tolerance test.",
        "Clinical Relevance": "Key indicator of diabetes. >140 mg/dL is pre-diabetic, >200 mg/dL suggests diabetes.",
        "Normal Range": "70 - 140 mg/dL (post-prandial)"
    },
    {
        "Variable": "BloodPressure",
        "Description": "Diastolic blood pressure (mm Hg).",
        "Clinical Relevance": "Hypertension is a commercially associated risk factor.",
        "Normal Range": "60 - 80 mm Hg"
    },
    {
        "Variable": "SkinThickness",
        "Description": "Triceps skin fold thickness (mm).",
        "Clinical Relevance": "Indicator of body fat and obesity.",
        "Normal Range": "10 - 50 mm (varies by gender/age)"
    },
    {
        "Variable": "Insulin",
        "Description": "2-Hour serum insulin (mu U/ml).",
        "Clinical Relevance": "High levels may indicate insulin resistance.",
        "Normal Range": "16 - 166 mu U/ml"
    },
    {
        "Variable": "BMI",
        "Description": "Body mass index (weight in kg/(height in m)^2).",
        "Clinical Relevance": "Major risk factor for Type 2 Diabetes.",
        "Normal Range": "18.5 - 24.9 kg/m²"
    },
    {
        "Variable": "DiabetesPedigreeFunction",
        "Description": "Diabetes pedigree function.",
        "Clinical Relevance": "Scores likelihood of diabetes based on family history.",
        "Normal Range": "0.08 - 2.42 (in dataset context)"
    },
    {
        "Variable": "Age",
        "Description": "Age (years).",
        "Clinical Relevance": "Risk increases with age.",
        "Normal Range": "N/A"
    }
]

df = pd.DataFrame(data)

st.table(df)

st.markdown("### References")
st.markdown("""
- American Diabetes Association Standards of Care
- National Institute of Diabetes and Digestive and Kidney Diseases
""")

render_footer()
