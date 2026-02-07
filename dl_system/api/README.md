---
title: Diabetes Disease Outcome AI System DL
emoji: 🧠
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🧠 Healthcare AI Systems: Inference API

## Overview

The core inference engine of the **Diabetes Disease Outcome Prediction System** is a high-performance **FastAPI** application. It serves:
1.  **Deep Learning Predictions**: Utilizing a custom Keras model trained on clinical data.
2.  **Explainable AI (XAI)**: Providing SHAP (SHapley Additive exPlanations) values via DeepExplainer.
3.  **Health Monitoring**: Real-time system status checks.

This API is designed for scalability, security, and ease of integration.

---

## 🛠️ Technology Stack

-   **Framework**: FastAPI (Python 3.10+)
-   **Model Runtime**: TensorFlow / Keras 2.18
-   **Explainability**: SHAP (DeepExplainer)
-   **Data Processing**: Pandas, Scikit-Learn (Pipelines)
-   **Validation**: Pydantic v2
-   **Server**: Uvicorn

---

## 🚀 Getting Started

### 1. Environment Setup

Create a `.env` file in the `api/` directory (or use system variables):

```env
# API Configuration
PROJECT_NAME="Diabetes Risk Prediction API"
VERSION="1.0.0"
API_V1_STR="/api/v1"

# Security
API_KEY="pneumonoultramicroscopicsilicovolcanoconiosis" # Example Key
ALLOWED_ORIGINS=["http://localhost:8501"] # Allow Client Access
```

### 2. Run the Server

Using `uv` (recommended) for fast dependency resolution:

```bash
uv sync
uv run uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

*The API will be available at `http://localhost:7860`.*

---

## 📚 API Reference

Interact with the autodocs at: **[http://localhost:7860/docs](http://localhost:7860/docs)**

### Key Endpoints

#### `POST /api/v1/predict`
Calculates the probability of diabetes onset based on patient vitals.
-   **Input**: JSON payload matching the `Patient` schema (Pregnancies, Glucose, BMI, Age, etc.).
-   **Output**: `probability` (0-1), `threshold`, `outcome` (0/1), and `metadata`.
-   **Security**: Requires `X-API-Key` header.

#### `POST /api/v1/explain`
Generates feature importance scores (SHAP values) for a specific patient.
-   **Input**: Same `Patient` JSON payload.
-   **Output**: List of feature contributions (Base value + SHAP values).
-   **Use Case**: Powering the "Model Explanation" UI.

#### `GET /health`
System status check.
-   **Response**: `{"status": "healthy", "model_loaded": true, ...}`.
-   **Checks**: Model artifacts, background referencing data, and server uptime.

---

## 🧬 Model Details

The underlying model is a **Feed-Forward Neural Network (MLP)** optimized for tabular data:
-   **Architecture**: Dense layers with ReLU activation, Batch Normalization, and Dropout regularization.
-   **Calibration**: Post-hoc Temperature Scaling ensures predicted probabilities reflect true empirical risk.
-   **Preprocessing**: Robust scaling and imputation pipelines (Scikit-Learn).

---

## 🛡️ Security Best Practices

-   **Authentication**: All predictive endpoints are protected by API Key middleware.
-   **Input Validation**: Strict type checking via Pydantic prevents injection attacks and malformed data.
-   **CORS**: Configurable Cross-Origin Resource Sharing to control client access.

---
*© 2026 Healthcare AI Systems (API)*
