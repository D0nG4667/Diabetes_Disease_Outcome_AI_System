# 🏥 Healthcare AI Systems: Clinical Client

## Overview

The user-facing component of the **Diabetes Disease Outcome Prediction System** is a sophisticated **Streamlit** dashboard. It empowers clinicians to interact with the underlying deep learning model in a intuitive, visually rich environment.

## ✨ Key Features

-   **Risk Prediction**: Instant single-patient analysis with clear risk indicators (High/Low).
-   **Explainable AI (XAI)**: Visualizes feature contributions (Glucose, BMI, etc.) using SHAP values.
-   **Batch Processing**: Screen entire cohorts by uploading CSV datasets.
-   **System Health**: Real-time monitoring of backend connectivity, authentication, and model readiness.
-   **Design System**: Custom CSS ("Glassmorphism") for a modern, professional clinical aesthetic.

---

## 🚀 Getting Started

### 1. Environment Setup

Create a `.env` file in the `client/` directory:

```env
# API Connection
DL_API_URL="http://localhost:8000/api/v1"
DL_API_KEY="pneumonoultramicroscopicsilicovolcanoconiosis" # Must match API config

# UI Settings
PAGE_TITLE="Diabetes Risk AI"
PAGE_ICON="🏥"
```

### 2. Run the Interface

Open a terminal in the `client/` directory:

```bash
uv sync # Install Streamlit, Requests, Pandas
uv run streamlit run Home.py
```

*Access the dashboard at `http://localhost:8501`.*

---

## 🎨 User Interface (UI) Components

The application is built with a modular component library for consistency:

1.  **Risk Cards**: Color-coded (Red/Green) containers displaying probabilities and outcomes.
2.  **Interactive SHAP Plots**: Detailed feature attribution using Plotly.
3.  **Sidebar Status**: Granular system health indicators (🟢 Online, 🔑 Auth Valid, 🧠 Model Ready).
4.  **Batch Uploader**: Drag-and-drop CSV processing with template download support.

---

## 🛡️ Clinical Guidelines

This client app includes dedicated documentation pages:
-   **Model Card**: Performance metrics, limitations, and training data details.
-   **Data Dictionary**: Definitions and ranges for all input features.
-   **Clinical Safety**: Disclaimers and usage protocols.

---
*© 2026 Healthcare AI Systems (Client)*
