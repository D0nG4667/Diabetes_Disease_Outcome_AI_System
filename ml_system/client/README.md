# DDOPS-AI: Clinical Dashboard

[![Interface](https://img.shields.io/badge/Streamlit-1.42-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Visualization](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=flat-square&logo=plotly)](https://plotly.com)
[![UX](https://img.shields.io/badge/User_Experience-Clinical_Grade-success?style=flat-square)](https://github.com/gabcares)

## 🖥️ Overview

The **DDOPS-AI Client** is a specialized interface designed for healthcare providers. It translates complex machine learning outputs into actionable clinical insights. Built with proper interaction design principles, it mitigates alert fatigue by presenting clear, color-coded risk assessments and prioritizing "human-in-the-loop" decision making.

### Key Modules

1.  **Risk Prediction (`Home` & `Risk Prediction`)**:
    - **Single Patient**: Form-based entry with validation toast notifications.
    - **Batch Assessment**: CSV upload capability for processing population cohorts.
2.  **Model Explanation (XAI)**:
    - Interactive **Plotly** visualizations utilizing SHAP values.
    - **Risk (Red)** vs. **Protective (Green)** color coding for intuitive interpretation.
    - Global feature impact distribution.
3.  **Clinical Safety & Data**:
    - **Model Cards**: Transparent documentation of model limitations and metrics.
    - **Data Dictionary**: Definitions of clinical variables to ensure standardized input.
    - **Safety Guidelines**: Protocols for interpreting AI-assisted outputs.

---

## 🎨 Design System

The application utilizes a custom theme optimized for readability in clinical environments:
- **Primary Color**: Emerald Green (`#10b981`) - Promoting a sense of calm and precision.
- **Visual Hierarchy**: Critical alerts (High Risk) are highlighted in Red/Orange to capture immediate attention.
- **Typography**: Sans-serif (Inter/Roboto) for screen legibility.

---

## 🚀 Usage Guide

### 1. Assessment
Navigate to **Risk Prediction**. Enter patient vitals.
> *Tip*: Use the "TAB" key to quickly move between input fields.

### 2. Interpretation
If a patient is flagged as high risk (or if clinically curious), navigate to **Model Explanation**.
- The **Bar Chart** shows the top features driving the specific prediction.
- **Negative values (Green)** indicate factors lowering the risk.
- **Positive values (Red)** indicate factors increasing the risk.

### 3. Reporting
For batch predictions, download the `batch_results.csv` to integrate with Electronic Health Records (EHR) or for further analysis.

---

## ⚙️ Configuration

The client connects to the backend via the `ML_API_URL` environment variable.

**`.env` Setup**:
```ini
ML_API_URL=http://api:7860  # For Docker Internal Network
# ML_API_URL=http://localhost:7860  # For Local Dev
```

### Running Locally
```bash
cd client
uv run streamlit run Home.py
```

---

**Medical Disclaimer**: This system generates probabilistic risk scores based on statistical patterns. It creates a hypothesis for clinical investigation, not a definitive diagnosis.

*User Experience Lead: Dr. Gabriel Okundaye*
