# 🏥 Healthcare AI Systems: Diabetes Disease Outcome Prediction

![System Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%2B%20Streamlit%20%2B%20TensorFlow-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🌟 Executive Summary

This project implements a **state-of-the-art Clinical Decision Support System (CDSS)** designed to predict diabetes disease outcomes with high interpretability and reliability. By integrating **Deep Learning (TensorFlow/Keras)** with **Explainable AI (SHAP)**, the system provides clinicians not just with a risk score, but with actionable insights into *why* a prediction was made.

The architecture decouples the inference engine (FastAPI Backend) from the clinical interface (Streamlit Client), ensuring scalability, security, and ease of deployment.

---

## 🏗️ System Architecture

The solution is composed of two primary microservices:

1.  **🧠 Inference Engine (`/api`)**: A high-performance FastAPI backend serving the deep learning model.
    -   **Model**: Neural Network with Dropout & Batch Normalization.
    -   **Calibration**: Temperature Scaling for probability accuracy.
    -   **Explainability**: DeepExplainer (SHAP) for feature attribution.
    -   **Security**: API Key authentication & robust input validation.

2.  **🩺 Clinical Interface (`/client`)**: An interactive Streamlit frontend for healthcare professionals.
    -   **Real-time Analysis**: Single-patient risk assessment.
    -   **Batch Processing**: CSV upload for population health screening.
    -   **Visualizations**: Interactive SHAP plots & risk dashboards.
    -   **Safety**: Built-in clinical disclaimers and data privacy execution.

---

## 🚀 Quick Start Guide

Prerequisites: Python 3.12+, `uv` (recommended) or `pip`.

### 1. Clone & Configure
```bash
git clone https://github.com/D0nG4667/Diabetes_Disease_Outcome_AI_System.git
cd Diabetes_Disease_Outcome_AI_System
cd dl_system
```

### 2. Launch the Backend (API)
The backend must be running first to serve predictions.
```bash
cd api
# Install dependencies
uv sync
# Run the server
uv run uvicorn sentry_app:app --host 0.0.0.0 --port 8000 --reload
```
*Health Check: http://localhost:8000/docs*

### 3. Launch the Frontend (Client)
Open a new terminal.
```bash
cd client
# Install dependencies
uv sync
# Run the interface
uv run streamlit run Home.py
```
*Access UI: http://localhost:8501*

---

## 🔐 Key Features

| Feature | Description | Tech Stack |
| :--- | :--- | :--- |
| **Deep Learning** | Custom-trained Neural Network for non-linear pattern recognition. | TensorFlow, Keras |
| **Model Calibration** | Post-hoc temperature scaling to ensure `Predicted Risk %` matches empirical risk. | Scikit-Learn |
| **Explainability** | Individual prediction explanations (Local) and global feature importance. | SHAP (DeepExplainer) |
| **API Security** | API Key header validation (`X-API-Key`) and comprehensive error handling. | FastAPI Security |
| **Batch Inference** | Process hundreds of patient records simultaneously with robust error handling. | Pandas, AsyncIO |

---

## 👨‍⚕️ Clinical usage

**Intended Use**: This tool is designed as a **screening aid** and **reasoning support tool** for clinicians. It analyzes physiological markers (Glucose, BMI, Age, etc.) to estimate the likelihood of diabetes onset.

**Disclaimer**: *This system is for investigational use and does not replace professional medical diagnosis. All predictions should be verified with standard confirmatory tests (e.g., HbA1c).*

---

## 📬 Contact & Support

**Principal Data Scientist**: Dr. Gabriel Okundaye  
**Focus**: Healthcare AI, MLOps, Clinical Informatics

---
*© 2026 Healthcare AI Systems. All Rights Reserved.*
