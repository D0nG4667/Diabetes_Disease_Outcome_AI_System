# Diabetes Disease Outcome Prediction System (DDOPS-AI)

[![System Status](https://img.shields.io/badge/System-Production%20Ready-success?style=flat-square&logo=docker)](https://github.com/gabcares)
[![Clinical Grade](https://img.shields.io/badge/Precision-Clinical%20Grade%20(90%2B)-blueviolet?style=flat-square)](https://github.com/gabcares)
[![XAI](https://img.shields.io/badge/Explainability-SHAP-orange?style=flat-square)](https://github.com/shap/shap)

## 🏥 Clinical Decision Support System (CDSS)

**DDOPS-AI** is a state-of-the-art, modular Machine Learning ecosystem designed to assist healthcare professionals in the early assessment of diabetes risk. By synthesizing clinical biomarkers—such as glucose levels, BMI, and age—with advanced **Ensemble Learning (XGBoost)** and **Explainable AI (SHAP)**, the system provides accurate, interpretable risk stratifications.

> **Disclaimer**: This tool is intended for *Clinical Decision Support* only. It does not replace professional medical diagnosis. All predictions should be validated by a qualified clinician.

---

## 🏗️ System Architecture

The system follows a microservices-based architecture, ensuring decoupling between inference logic and user interaction layer.

```mermaid
graph LR
    User[Clinician / User] -->|HTTPS| Client[Streamlit Client (Frontend)]
    Client -->|REST API (JSON)| API[FastAPI Inference Engine (Backend)]
    API -->|Load| Model[XGBoost Classifier]
    API -->|Compute| SHAP[SHAP Explainer]
    API -->|Response| Client
    Client -->|Visualize| Plot[Plotly Interactive Charts]
```

### Components

| Service | Technology | Role |
| :--- | :--- | :--- |
| **Inference Engine** | `FastAPI`, `XGBoost`, `Pandas` | Handles predictive modeling, data validation, and real-time SHAP explanation generation. |
| **Clinical Client** | `Streamlit`, `Plotly` | Provides an intuitive interface for single-patient assessment, batch processing, and interactive model exploration. |
| **Orchestration** | `Docker Compose` | Manages container lifecycle, networking, and volume persistence. |

---

## 🚀 Quick Start (Production)

The entire system is containerized for seamless deployment.

### Prerequisites
- **Docker** & **Docker Compose**
- **Git**

### Deployment
1. **Clone the Repository**
   ```bash
   git clone https://github.com/D0nG4667/Diabetes_Disease_Outcome_AI_System.git
   cd Diabetes_Disease_Outcome_AI_System
   cd ml_system
   ```

2. **Launch Services**
   ```bash
   docker compose up --build -d
   ```

3. **Access Interfaces**
   - **Clinical Dashboard**: [http://localhost:8501](http://localhost:8501)
   - **API Documentation (Swagger UI)**: [http://localhost:7860/docs](http://localhost:7860/docs)

---

## 🧪 Clinical Workflow

The system supports two primary workflows tailored for hospital settings:

1.  **Individual Assessment**:
    - Clinician enters patient vitals manually during consultation.
    - System returns immediate risk probability (0-100%) and binary outcome.
    - **Explainability**: SHAP visualization breaks down *why* the risk is high/low (e.g., "High Glucose increased risk by +0.2").

2.  **Population Health (Batch Processing)**:
    - Upload CSV datasets containing multiple patient records.
    - System processes records asynchronously and returns a comprehensive risk report.
    - Useful for screening drives or retrospective analysis.

## 🛠️ Development & Contribution

### Directory Structure
- `api/`: Backend service logic, model artifacts, and core library.
- `client/`: Frontend application, UI components, and state management.
- `data/`: Sample datasets and data dictionaries.

### Environment Configuration
Copy `.env.example` to `.env` in both `client/` and `api/` directories to configure service URLs and debug modes.

---

**© 2026 Healthcare AI Systems.**
*Principal Architect: Dr. Gabriel Okundaye*
