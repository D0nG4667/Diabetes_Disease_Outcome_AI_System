import streamlit as st
from utils.ui_components import load_css, render_header, render_sidebar_info, render_footer

st.set_page_config(page_title="Model Card", page_icon="🔍", layout="wide")
load_css()

render_header("🔍 DL Model Card", "Clinical MLP Classifier (Optuna Optimized)")

st.markdown("""
### Model Details
- **Model Name**: `best_clinical_mlp_classifier_optuna`
- **Version**: `1.0.0`
- **Type**: Deep Learning Classifier (Feed-Forward Neural Network)
- **Framework**: TensorFlow / Keras 2.x
- **Optimization**: Optuna Hyperparameter Tuning (Bayesian Optimization)

### Architecture
- **Input Layer**: 30 features (after one-hot encoding & scaling)
- **Hidden Layers**: Dynamic (2-4 layers), Relu activation, Batch Normalization, Dropout (0.2-0.5).
- **Output Layer**: Sigmoid activation (Binary Classification).
- **Loss Function**: Focal Loss (handling class imbalance).
- **Optimizer**: Adam (Adaptive Learning Rate).

### Performance Metrics (Test Set)
| Metric | Value |
|--------|-------|
| **Recall (Sensitivity)** | >0.83 (Clinically Constraint) |
| **Precision** | ~0.45 (Alert fatigue) |
| **ROC-AUC** | 0.75 |

### Intended Use
- **Primary Use**: Screening tool to identify patients at high risk of diabetes who require confirmatory testing.
- **Target Population**: Adults > 21 years old.
- **Out of Scope**: Pediatric patients, Type 1 Diabetes diagnosis.

### Limitations & Biases
- **Data Bias**: Trained on PIMA Indians Diabetes Dataset (specific demographic). Generalizability to other populations requires validation.
- **Imputation**: Model relies on imputed values for missing skin thickness/insulin data.
- **Sensitivity**: Optimized for high recall (to minimize false negatives), which may result in higher false positives.

### Ethical Considerations
- **Fairness**: Efforts made to balance recall across age groups.
- **Transparency**: SHAP integration provided for individual level explanation.
""")

render_sidebar_info()
render_footer()
