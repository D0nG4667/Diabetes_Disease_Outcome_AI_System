---
title: Diabetes Disease Outcome AI System ML
emoji: 🩺
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# DDOPS-AI: Inference & Explanation Engine

[![Framework](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Model](https://img.shields.io/badge/XGBoost-Ranking_Model-red?style=flat-square)](https://xgboost.readthedocs.io)
[![Standards](https://img.shields.io/badge/OpenAPI-3.0-green?style=flat-square)](https://swagger.io)

## 🧠 Core Functionality

The **API Microservice** serves as the computational brain of the Diabetes Prediction System. It is engineered for low-latency inference and high-fidelity model interpretability. It exposes RESTful endpoints to accept clinical data, validate inputs against physiological constraints, and return both probabilistic predictions and feature-level explanations.

### Key Capabilities

1.  **Predictive Modeling**: Utilizes a pre-trained, calibrated **XGBoost Classifier** optimized for Recall (sensitivity) to minimize false negatives in disease screening.
2.  **Explainable AI (XAI)**: Integrates **SHAP (SHapley Additive exPlanations)** to provide local interpretability for every prediction. It generates both raw SHAP values and pre-rendered visualization assets (via `kaleido`/`plotly`).
3.  **Data Validation**: Implements strict Pydantic schemas to ensure data integrity (e.g., rejecting negative ages or impossible BMI values).

---

## 🔌 API Specification

### Base URL: `http://localhost:7860`

### Endpoints

#### 1. Prediction (`POST /api/v1/predict`)
Performs binary classification on patient physiological data.

- **Request Body**:
  ```json
  {
    "pregnancies": 2,
    "glucose": 140,
    "blood_pressure": 85,
    "skin_thickness": 30,
    "insulin": 100,
    "bmi": 32.5,
    "diabetes_pedigree_function": 0.6,
    "age": 45
  }
  ```
- **Response**:
  ```json
  {
    "outcome": 1,
    "probability": 0.78,
    "threshold": 0.45,
    "model_version": "1.0.0"
  }
  ```

#### 2. Explanation (`POST /api/v1/explain`)
Detail analysis of *why* a specific prediction was made.

- **Parameters**: `top_n` (default: 10), `plot` (boolean)
- **Response**:
  - `shap_values`: Raw feature contribution scores.
  - `shap_plot_base64`: Base64-encoded PNG of the feature impact distribution (if `plot=true`).

---

## 🛠️ Technical Stack & Setup

### Dependencies
- **Runtime**: Python 3.10+
- **Serving**: `Uvicorn` (ASGI)
- **ML Libraries**: `scikit-learn`, `xgboost`, `shap`, `pandas`
- **Visualization**: `plotly`, `kaleido` (for backend image generation)

### Local Development

1.  **Install Dependencies**:
    ```bash
    cd api
    uv sync  # or pip install -r requirements.txt
    ```

2.  **Run Server**:
    ```bash
    uv run uvicorn app:app --host 0.0.0.0 --port 7860 --reload
    ```

### Docker Deployment

The service is fully defined in the project's `docker-compose.yml`. To rebuild the API specifically (e.g., after adding dependencies):

```bash
docker compose build api
docker compose up -d api
```

---

## 🩺 Model Governance

- **Model Type**: Ensemble Gradient Boosting (XGBoost)
- **Training Data**: PIMA Indians Diabetes Dataset (Standardized)
- **Primary Metric**: Recall (Sensitivity) > 0.85
- **Input Constraints**:
    - `glucose`: 0 - 300 mg/dL
    - `bmi`: 0 - 70 kg/m²
    - `age`: 0 - 120 years

*API Developer: DonG4667*
