import streamlit as st
from utils.ui_components import load_css, render_header, render_sidebar_info, render_footer

st.set_page_config(page_title="Data Dictionary", page_icon="📘", layout="wide")
load_css()

render_header("📘 Data Dictionary", "Input Variables & Clinical Context")

data = [
    {"Variable": "Pregnancies", "Type": "Integer", "Description": "Number of times pregnant", "Normal Range": "0-20"},
    {"Variable": "Glucose", "Type": "Numeric", "Description": "Plasma glucose concentration a 2 hours in an oral glucose tolerance test", "Normal Range": "70-140 mg/dL"},
    {"Variable": "BloodPressure", "Type": "Numeric", "Description": "Diastolic blood pressure (mm Hg)", "Normal Range": "60-80 mm Hg"},
    {"Variable": "SkinThickness", "Type": "Numeric", "Description": "Triceps skin fold thickness (mm)", "Normal Range": "10-50 mm"},
    {"Variable": "Insulin", "Type": "Numeric", "Description": "2-Hour serum insulin (mu U/ml)", "Normal Range": "16-166 mu U/ml"},
    {"Variable": "BMI", "Type": "Numeric", "Description": "Body mass index (weight in kg/(height in m)^2)", "Normal Range": "18.5-24.9"},
    {"Variable": "DiabetesPedigreeFunction", "Type": "Numeric", "Description": "Diabetes pedigree function (likelihood of diabetes based on family history)", "Normal Range": "0.08-2.42"},
    {"Variable": "Age", "Type": "Integer", "Description": "Age (years)", "Normal Range": "21-81"},
]

st.table(data)

st.markdown("""
### Missing Data Handling
- **Glucose, BloodPressure, SkinThickness, Insulin, BMI**: Zeros in these fields represent missing values and are imputed by the preprocessing pipeline using KNN/Median imputation before model inference.
""")

render_sidebar_info()
render_footer()
