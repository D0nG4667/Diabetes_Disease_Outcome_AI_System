# **🩺 Diabetes Prediction – Healthcare AI Systems Capstone**  
<p align="center">
  <img src="https://img.shields.io/badge/AI%20for%20Healthcare-Diabetes%20Prediction-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/uv-Package%20Manager-0A7BBB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Ready-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-UI%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

This project develops two production‑ready AI systems—one Machine Learning (ML) and one Deep Learning (DL)—to predict **Type 2 Diabetes** using structured clinical data from the **Pima Indians Diabetes Dataset**. The work emphasizes clinical validity, responsible AI practices, and real‑world deployment workflows.

---

# **📌 1. Project Overview**

Diabetes is a rapidly growing global health challenge, affecting over 500 million adults worldwide. Early detection is critical for preventing complications such as cardiovascular disease, kidney failure, neuropathy, and blindness. However, traditional diagnostic pathways can be resource‑intensive and inaccessible in many settings.

This capstone builds **two independent AI systems** capable of predicting diabetes risk using routinely collected clinical variables such as:

- Glucose  
- BMI  
- Insulin  
- Blood Pressure  
- Age  
- Pregnancy history  
- Diabetes pedigree function  

The project follows a full **CRISP‑DM pipeline**, from data wrangling to deployment, with strong emphasis on:

- Clinical interpretability  
- Imbalance handling  
- Ethical considerations  
- Robust evaluation  
- Real‑world deployment  

---

# **📌 2. Key Features**

### **🔬 Machine Learning System**
- Logistic Regression, Random Forest, and Gradient Boosting models  
- Hyperparameter tuning with cross‑validation  
- SMOTE, class weights, and threshold tuning  
- SHAP‑based interpretability  
- FastAPI endpoint + Streamlit UI  
- Dockerized and deployed on Render  

### **🧠 Deep Learning System**
- Fully connected neural network with ≥3 hidden layers  
- Dropout + L2 regularization  
- Class‑weighted loss + oversampling  
- Learning curves and generalization analysis  
- FastAPI endpoint + Streamlit UI  
- Dockerized and deployed on Render  

---

# **📌 3. Dataset**

**Source:** Pima Indians Diabetes Dataset  
**Link:** https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database/data  

**Target Variable:**  
- `Outcome` (1 = diabetic, 0 = non‑diabetic)

**Predictor Variables:**  
- Pregnancies  
- Glucose  
- BloodPressure  
- SkinThickness  
- Insulin  
- BMI  
- DiabetesPedigreeFunction  
- Age  

**Important Note:** Several physiological features contain **zero values representing missingness**. These are handled carefully during preprocessing.

```folder
├── 📁 artifacts       # ML/DL artifacts (models, scalers, etc.)
├── 📁 data            # Raw and processed datasets
├── 📁 dl_system       # Deep Learning system (API + Streamlit Client)
├── 📁 ml_system       # Machine Learning system (API + Streamlit Client)
├── 📁 models          # Trained model files
├── 📁 notebooks       # Jupyter notebooks for EDA, preprocessing, and training
├── 📁 plots           # Generated plots and visualizations
├── 📁 reports         # Reports and ethical analysis
├── 📝 FILETREE.md     # Full file structure
├── 📝 LICENSE.md      # License information
└── 📝 README.md       # Project documentation
```

> **Note:** For a comprehensive view of the project structure, including all files and subdirectories, please refer to the [FILETREE.md](FILETREE.md).

---

# **📌 5. Methodology (CRISP‑DM)**

### **1. Data Wrangling**
- Replace physiologically impossible zeros with NaN  
- Median imputation for skewed variables  
- Outlier detection using IQR and clinical thresholds  
- Ensure no data leakage via pipelines  

### **2. Exploratory Data Analysis**
- Class imbalance visualization  
- Feature distributions (stratified by Outcome)  
- Correlation heatmaps  
- Clinical insights from patterns  

### **3. Preprocessing & Feature Engineering**
- Scaling with StandardScaler  
- Train/validation/test split (stratified)  
- Imbalance handling:  
  - SMOTE  
  - Random oversampling  
  - Class‑weighted loss  
  - Threshold tuning  

### **4. ML System**
- Logistic Regression  
- Random Forest  
- Gradient Boosting / XGBoost  
- Hyperparameter tuning  
- SHAP interpretability  

### **5. DL System**
- Dense neural network (≥3 layers)  
- Dropout + L2 regularization  
- Class‑weighted BCE loss  
- Early stopping  
- Learning curves  

### **6. Deployment**
- FastAPI endpoints for ML and DL  
- Streamlit apps for interactive prediction  
- Dockerized services  
- Render deployment  

---

# **📌 6. Evaluation Metrics**

Primary metrics (clinical priority):  
- **Recall (Sensitivity)**  
- **ROC‑AUC**

Secondary metrics:  
- Precision  
- F1‑Score  
- PR‑AUC  
- Confusion Matrix  

Clinical justification:  
> Missing a diabetic patient (false negative) can delay treatment and cause severe complications.  
> Therefore, **Recall is prioritized over Accuracy**.

---

# **📌 7. Deployment Links**

### **🔗 ML System**
- **Streamlit App:** *[https://diabetes-ml-system.streamlit.app/](https://diabetes-ml-system.streamlit.app/)*  
- **FastAPI Endpoint:** *[https://statogale-diabetes-disease-outcome-ai-system-ml.hf.space](https://statogale-diabetes-disease-outcome-ai-system-ml.hf.space)*  
- **Swagger Docs:** *[https://statogale-diabetes-disease-outcome-ai-system-ml.hf.space/docs](https://statogale-diabetes-disease-outcome-ai-system-ml.hf.space/docs)*  

### **🔗 DL System**
- **Streamlit App:** *[https://diabetes-dl-system.streamlit.app/](https://diabetes-dl-system.streamlit.app/)*  
- **FastAPI Endpoint:** *[https://statogale-diabetes-disease-outcome-ai-system-dl.hf.space](https://statogale-diabetes-disease-outcome-ai-system-dl.hf.space)*  
- **Swagger Docs:** *[https://statogale-diabetes-disease-outcome-ai-system-dl.hf.space/docs](https://statogale-diabetes-disease-outcome-ai-system-dl.hf.space/docs)*  

---

# **📌 8. How to Run Locally (uv + pyproject.toml)**

This project uses **uv** for fast and efficient dependency management. Each system component (ML/DL API & Client) maintains its own `pyproject.toml` for isolation.

### **1. Install uv**
(If not already installed)
```bash
pip install uv
```

### **2. Clone the repository**
```bash
git clone https://github.com/D0nG4667/Diabetes_Disease_Outcome_AI_System.git
cd Diabetes_Disease_Outcome_AI_System
```

### **3. Run the ML System**
**ML API:**
```bash
cd ml_system/api
uv run uvicorn app:app --reload
```

**ML Client:**
(Open a new terminal)
```bash
cd ml_system/client
uv run streamlit run Home.py
```

### **4. Run the DL System**
**DL API:**
```bash
cd dl_system/api
uv run uvicorn app:app --reload
```

**DL Client:**
(Open a new terminal)
```bash
cd dl_system/client
uv run streamlit run Home.py
```

### **5. Manage Dependencies**
To add a package to a specific component:
```bash
cd <component_directory>
uv add <package_name>
```

---

# **📌 9. Ethical Considerations**

- Dataset is limited to Pima Indian women → **limited demographic generalizability**  
- Risk of algorithmic bias if deployed without external validation  
- Models should support—not replace—clinical judgment  
- Requires calibration and prospective evaluation before real‑world use  

---

# **📌 10. References**

Alghamdi, M., Al‑Muhtadi, J., & Al‑Ghamdi, A. (2017). A comparative study of machine learning algorithms for predicting diabetes. *IJACSA, 8*(6).

Han, L., Luo, S., Yu, J., Pan, L., Chen, S., & Yang, D. (2020). Rule extraction from SVMs for diabetes diagnosis. *Healthcare, 8*(3), 247.

Rahman, M. M., & Islam, M. M. (2020). Exploring machine learning approaches for diabetes prediction. *Diabetes & Metabolic Syndrome, 14*(5), 1021–1025.

---

# **📌 11. License**

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.

[![CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc/4.0/)

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes.

For more details, see the [LICENSE.md](LICENSE.md) file.

### **📩 Commercial Inquiries**

For commercial licensing, custom implementations, or collaboration opportunities, please contact the author.

<br>
<hr>
<p align="center">
  <b>Made with ❤️ by <a href="https://linkedin.com/in/dr-gabriel-okundaye" target="_blank">Dr. Gabriel Okundaye</a></b>
  <br>
  🌐 <a href="https://gabcares.xyz" target="_blank">gabcares.xyz</a> &nbsp;|&nbsp; 🐙 <a href="https://github.com/D0nG4667" target="_blank">GitHub</a>
</p>

