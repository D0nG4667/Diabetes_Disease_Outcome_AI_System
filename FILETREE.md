# File Tree: Diabetes Disease Outcome ML DL

**Generated:** 2/7/2026, 7:06:36 AM

```
├── 📁 artifacts
│   ├── 📁 dl
│   │   ├── 📄 background_data.csv
│   │   └── ⚙️ dl_threshold.json
│   ├── 📁 eda
│   │   └── 📄 eda_artifacts.joblib
│   ├── 📁 ml
│   │   ├── ⚙️ ml_threshold.json
│   │   └── 📄 shap_background.joblib
│   └── 📁 preprocessing
│       └── 📄 preprocessing_artifacts.joblib
├── 📁 data
│   ├── 📁 processed
│   │   ├── 📄 X_eval.parquet
│   │   ├── 📄 X_test.parquet
│   │   ├── 📄 X_train.parquet
│   │   ├── 📄 y_eval.parquet
│   │   ├── 📄 y_test.parquet
│   │   └── 📄 y_train.parquet
│   └── 📁 raw
│       └── 📁 kaggle
│           └── 📄 diabetes.csv
├── 📁 dl_system
│   ├── 📁 api
│   │   ├── 📁 core
│   │   │   ├── 🐍 config.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   ├── 🐍 logging.py
│   │   │   └── 🐍 security.py
│   │   ├── 📁 models
│   │   │   └── 🐍 artifacts_loader.py
│   │   ├── 📁 routers
│   │   │   ├── 🐍 explain.py
│   │   │   ├── 🐍 health.py
│   │   │   └── 🐍 predict.py
│   │   ├── 📁 schemas
│   │   │   └── 🐍 patient.py
│   │   ├── 📁 services
│   │   │   ├── 🐍 explainer.py
│   │   │   └── 🐍 predictor.py
│   │   ├── 📁 templates
│   │   │   ├── 🌐 404.html
│   │   │   └── 🌐 index.html
│   │   ├── 📁 utils
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 feature_creation.py
│   │   │   ├── 🐍 preprocessing.py
│   │   │   ├── 🐍 shap_utils.py
│   │   │   └── 🐍 temperature_scaling.py
│   │   ├── ⚙️ .gitignore
│   │   ├── 🐳 Dockerfile
│   │   ├── 📝 README.md
│   │   ├── 🐍 app.py
│   │   ├── ⚙️ pyproject.toml
│   │   └── 📄 uv.lock
│   ├── 📁 client
│   │   ├── 📁 .streamlit
│   │   │   └── ⚙️ config.toml
│   │   ├── 📁 assets
│   │   │   ├── 📁 css
│   │   │   │   └── 🎨 style.css
│   │   │   └── 📁 logos
│   │   │       └── 🖼️ logo.png
│   │   ├── 📁 pages
│   │   │   ├── 🐍 1_📊_Risk_Prediction.py
│   │   │   ├── 🐍 2_🧠_Model_Explanation.py
│   │   │   ├── 🐍 3_📘_Data_Dictionary.py
│   │   │   ├── 🐍 4_🔍_Model_Card.py
│   │   │   └── 🐍 5_⚠️_Clinical_Safety.py
│   │   ├── 📁 utils
│   │   │   ├── 🐍 api_client.py
│   │   │   └── 🐍 ui_components.py
│   │   ├── ⚙️ .env.example
│   │   ├── 🐳 Dockerfile
│   │   ├── 🐍 Home.py
│   │   ├── 📝 README.md
│   │   ├── ⚙️ pyproject.toml
│   │   └── 📄 uv.lock
│   ├── ⚙️ .dockerignore
│   ├── 📝 README.md
│   └── ⚙️ docker-compose.yml
├── 📁 ml_system
│   ├── 📁 api
│   │   ├── 📁 core
│   │   │   ├── 🐍 config.py
│   │   │   ├── 🐍 exceptions.py
│   │   │   └── 🐍 logging.py
│   │   ├── 📁 models
│   │   │   └── 🐍 artifacts_loader.py
│   │   ├── 📁 routers
│   │   │   ├── 🐍 explain.py
│   │   │   ├── 🐍 health.py
│   │   │   └── 🐍 predict.py
│   │   ├── 📁 schemas
│   │   │   └── 🐍 patient.py
│   │   ├── 📁 services
│   │   │   ├── 🐍 explainer.py
│   │   │   └── 🐍 predictor.py
│   │   ├── 📁 templates
│   │   │   ├── 🌐 404.html
│   │   │   └── 🌐 index.html
│   │   ├── 📁 utils
│   │   │   ├── 🐍 constants.py
│   │   │   ├── 🐍 feature_creation.py
│   │   │   ├── 🐍 preprocessing.py
│   │   │   └── 🐍 shap_utils.py
│   │   ├── ⚙️ .gitignore
│   │   ├── 🐳 Dockerfile
│   │   ├── 📝 README.md
│   │   ├── 🐍 app.py
│   │   ├── ⚙️ pyproject.toml
│   │   ├── 📄 run.bat
│   │   └── 📄 uv.lock
│   ├── 📁 client
│   │   ├── 📁 .streamlit
│   │   │   └── ⚙️ config.toml
│   │   ├── 📁 assets
│   │   │   ├── 📁 css
│   │   │   └── 📁 logos
│   │   ├── 📁 pages
│   │   │   ├── 🐍 1_📊_Risk_Prediction.py
│   │   │   ├── 🐍 2_🧠_Model_Explanation.py
│   │   │   ├── 🐍 3_📘_Data_Dictionary.py
│   │   │   ├── 🐍 4_🔍_Model_Card.py
│   │   │   └── 🐍 5_⚠️_Clinical_Safety.py
│   │   ├── 📁 utils
│   │   │   ├── 🐍 api.py
│   │   │   └── 🐍 ui_components.py
│   │   ├── ⚙️ .env.example
│   │   ├── ⚙️ .gitignore
│   │   ├── 🐳 Dockerfile
│   │   ├── 🐍 Home.py
│   │   ├── 📝 README.md
│   │   ├── ⚙️ pyproject.toml
│   │   └── 📄 uv.lock
│   ├── ⚙️ .dockerignore
│   ├── 📝 README.md
│   └── ⚙️ docker-compose.yml
├── 📁 models
│   ├── 📁 dl
│   │   ├── 📁 plots
│   │   │   ├── 🌐 pdp_age_w_f.html
│   │   │   ├── 🌐 pdp_age_wo_f.html
│   │   │   ├── 🌐 pdp_age_x_dpf_w_f.html
│   │   │   ├── 🌐 pdp_blood_pressure_missing_w_f.html
│   │   │   ├── 🌐 pdp_blood_pressure_w_f.html
│   │   │   ├── 🌐 pdp_blood_pressure_wo_f.html
│   │   │   ├── 🌐 pdp_bmi_missing_w_f.html
│   │   │   ├── 🌐 pdp_bmi_w_f.html
│   │   │   ├── 🌐 pdp_bmi_wo_f.html
│   │   │   ├── 🌐 pdp_diabetes_pedigree_function_w_f.html
│   │   │   ├── 🌐 pdp_diabetes_pedigree_function_wo_f.html
│   │   │   ├── 🌐 pdp_glucose_missing_w_f.html
│   │   │   ├── 🌐 pdp_glucose_w_f.html
│   │   │   ├── 🌐 pdp_glucose_wo_f.html
│   │   │   ├── 🌐 pdp_glucose_x_bmi_w_f.html
│   │   │   ├── 🌐 pdp_insulin_missing_w_f.html
│   │   │   ├── 🌐 pdp_insulin_wo_f.html
│   │   │   ├── 🌐 pdp_pregnancies_w_f.html
│   │   │   ├── 🌐 pdp_pregnancies_wo_f.html
│   │   │   ├── 🌐 pdp_pregnancies_x_glucose_w_f.html
│   │   │   ├── 🌐 pdp_skin_thickness_missing_w_f.html
│   │   │   ├── 🌐 pdp_skin_thickness_wo_f.html
│   │   │   ├── 🌐 shap_strip_w_f.html
│   │   │   └── 🌐 shap_strip_wo_f.html
│   │   ├── 📄 best_clinical_mlp_classifier_optuna.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v1.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v10.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v11.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v12.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v13.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v14.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v15.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v16.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v17.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v18.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v19.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v2.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v20.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v21.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v22.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v23.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v24.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v25.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v26.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v27.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v28.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v29.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v3.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v4.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v5.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v6.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v7.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v8.keras
│   │   ├── 📄 best_clinical_mlp_classifier_optuna_v9.keras
│   │   ├── 📄 feature_creator.joblib
│   │   ├── 📄 preprocessor.joblib
│   │   └── 📄 temperature_scaler.keras
│   └── 📁 ml
│       ├── 📄 DecisionTreeClassifier__SMOTE.joblib
│       ├── 📄 LogisticRegression__SMOTETomek.joblib
│       ├── 📄 RandomForestClassifier__SMOTETomek.joblib
│       ├── 📄 XGBClassifier__RandomUnderSampler.joblib
│       ├── 📄 feature_creator.joblib
│       ├── 📄 label_encoder.joblib
│       └── 📄 preprocessor.joblib
├── 📁 notebooks
│   ├── 📁 studies
│   │   ├── 📁 dl_optuna_study_v1
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v10
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v11
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v12
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v13
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v14
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v15
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v16
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v17
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v18
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v19
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v2
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v20
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v22
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v23
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v24
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v25
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v26
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v27
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v28
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v29
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v3
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v30
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v4
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v5
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v6
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v7
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v8
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 feature_creator.joblib
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📁 dl_optuna_study_v9
│   │   │   ├── 📁 dashboards
│   │   │   │   ├── 🌐 contour.html
│   │   │   │   ├── 🌐 optimization_history.html
│   │   │   │   ├── 🌐 parallel_coordinate.html
│   │   │   │   ├── 🌐 param_importances.html
│   │   │   │   └── 🌐 slice.html
│   │   │   ├── 📄 preprocessor.joblib
│   │   │   └── 📝 study_card.md
│   │   ├── 📄 dl_optuna_study_v1.db
│   │   ├── 📄 dl_optuna_study_v10.db
│   │   ├── 📄 dl_optuna_study_v11.db
│   │   ├── 📄 dl_optuna_study_v12.db
│   │   ├── 📄 dl_optuna_study_v13.db
│   │   ├── 📄 dl_optuna_study_v14.db
│   │   ├── 📄 dl_optuna_study_v15.db
│   │   ├── 📄 dl_optuna_study_v16.db
│   │   ├── 📄 dl_optuna_study_v17.db
│   │   ├── 📄 dl_optuna_study_v18.db
│   │   ├── 📄 dl_optuna_study_v19.db
│   │   ├── 📄 dl_optuna_study_v2.db
│   │   ├── 📄 dl_optuna_study_v20.db
│   │   ├── 📄 dl_optuna_study_v21.db
│   │   ├── 📄 dl_optuna_study_v22.db
│   │   ├── 📄 dl_optuna_study_v23.db
│   │   ├── 📄 dl_optuna_study_v24.db
│   │   ├── 📄 dl_optuna_study_v25.db
│   │   ├── 📄 dl_optuna_study_v26.db
│   │   ├── 📄 dl_optuna_study_v27.db
│   │   ├── 📄 dl_optuna_study_v28.db
│   │   ├── 📄 dl_optuna_study_v29.db
│   │   ├── 📄 dl_optuna_study_v3.db
│   │   ├── 📄 dl_optuna_study_v30.db
│   │   ├── 📄 dl_optuna_study_v4.db
│   │   ├── 📄 dl_optuna_study_v5.db
│   │   ├── 📄 dl_optuna_study_v6.db
│   │   ├── 📄 dl_optuna_study_v7.db
│   │   ├── 📄 dl_optuna_study_v8.db
│   │   └── 📄 dl_optuna_study_v9.db
│   ├── 📁 utils
│   │   ├── 🐍 cleaning.py
│   │   ├── 🐍 constants.py
│   │   ├── 🐍 feature_creation.py
│   │   ├── 🐍 feature_selector.py
│   │   ├── 🐍 paths.py
│   │   └── 🐍 visualisation.py
│   ├── ⚙️ .gitignore
│   ├── 📄 01_eda.ipynb
│   ├── 📄 02_preprocessing.ipynb
│   ├── 📄 03_ml_models.ipynb
│   ├── 📄 04_dl_models.ipynb
│   ├── ⚙️ pyproject.toml
│   └── 📄 uv.lock
├── 📁 plots
│   ├── 🖼️ age_bin_vs_outcome_proportion.webp
│   ├── 🖼️ association_strength_with_heart_disease_cram_r_s_v.webp
│   ├── 🖼️ blood_pressure_bin_vs_outcome_proportion.webp
│   ├── 🖼️ bmi_bin_vs_outcome_proportion.webp
│   ├── 🖼️ class_distribution_outcome.webp
│   ├── 🖼️ confusion_matrix_class_weight.webp
│   ├── 🖼️ confusion_matrix_class_weight_thr_0_10.webp
│   ├── 🖼️ confusion_matrix_class_weight_thr_0_40.webp
│   ├── 🖼️ confusion_matrix_class_weight_threshold.webp
│   ├── 🖼️ confusion_matrix_class_weight_threshold_thr_0_10.webp
│   ├── 🖼️ confusion_matrix_class_weight_threshold_thr_0_20.webp
│   ├── 🖼️ confusion_matrix_class_weight_threshold_thr_0_46.webp
│   ├── 🖼️ confusion_matrix_decisiontreeclassifier_randomoversampler.webp
│   ├── 🖼️ confusion_matrix_decisiontreeclassifier_randomundersampler.webp
│   ├── 🖼️ confusion_matrix_decisiontreeclassifier_smote.webp
│   ├── 🖼️ confusion_matrix_logisticregression_none.webp
│   ├── 🖼️ confusion_matrix_logisticregression_randomoversampler.webp
│   ├── 🖼️ confusion_matrix_logisticregression_randomundersampler.webp
│   ├── 🖼️ confusion_matrix_logisticregression_smote.webp
│   ├── 🖼️ confusion_matrix_logisticregression_smotetomek.webp
│   ├── 🖼️ confusion_matrix_none.webp
│   ├── 🖼️ confusion_matrix_none_thr_0_10.webp
│   ├── 🖼️ confusion_matrix_none_thr_0_20.webp
│   ├── 🖼️ confusion_matrix_none_thr_0_39.webp
│   ├── 🖼️ confusion_matrix_oversample.webp
│   ├── 🖼️ confusion_matrix_oversample_class_weight.webp
│   ├── 🖼️ confusion_matrix_oversample_class_weight_thr_0_30.webp
│   ├── 🖼️ confusion_matrix_oversample_class_weight_thr_0_32.webp
│   ├── 🖼️ confusion_matrix_oversample_class_weight_thr_0_34.webp
│   ├── 🖼️ confusion_matrix_oversample_class_weight_threshold.webp
│   ├── 🖼️ confusion_matrix_oversample_class_weight_threshold_thr_0_35.webp
│   ├── 🖼️ confusion_matrix_oversample_class_weight_threshold_thr_0_45.webp
│   ├── 🖼️ confusion_matrix_oversample_thr_0_10.webp
│   ├── 🖼️ confusion_matrix_oversample_thr_0_25.webp
│   ├── 🖼️ confusion_matrix_oversample_thr_0_39.webp
│   ├── 🖼️ confusion_matrix_oversample_thr_0_48.webp
│   ├── 🖼️ confusion_matrix_oversample_threshold.webp
│   ├── 🖼️ confusion_matrix_oversample_threshold_thr_0_30.webp
│   ├── 🖼️ confusion_matrix_oversample_threshold_thr_0_32.webp
│   ├── 🖼️ confusion_matrix_oversample_threshold_thr_0_37.webp
│   ├── 🖼️ confusion_matrix_randomforestclassifier_randomoversampler.webp
│   ├── 🖼️ confusion_matrix_randomforestclassifier_randomundersampler.webp
│   ├── 🖼️ confusion_matrix_randomforestclassifier_smotetomek.webp
│   ├── 🖼️ confusion_matrix_threshold.webp
│   ├── 🖼️ confusion_matrix_threshold_thr_0_20.webp
│   ├── 🖼️ confusion_matrix_threshold_thr_0_28.webp
│   ├── 🖼️ confusion_matrix_threshold_thr_0_39.webp
│   ├── 🖼️ confusion_matrix_xgbclassifier_randomundersampler.webp
│   ├── 🖼️ confusion_matrix_xgbclassifier_smote.webp
│   ├── 🖼️ confusion_matrix_xgbclassifier_smotetomek.webp
│   ├── 🖼️ diabetes_prevalence_by_glucose_and_bmi_bins.webp
│   ├── 🖼️ distribution_of_patients_in_the_age_column_by_outcome.webp
│   ├── 🖼️ distribution_of_patients_in_the_blood_pressure_column_by_outcome.webp
│   ├── 🖼️ distribution_of_patients_in_the_bmi_column_by_outcome.webp
│   ├── 🖼️ distribution_of_patients_in_the_diabetes_pedigree_function_column_by_outcome.webp
│   ├── 🖼️ distribution_of_patients_in_the_glucose_column_by_outcome.webp
│   ├── 🖼️ distribution_of_patients_in_the_insulin_column_by_outcome.webp
│   ├── 🖼️ distribution_of_patients_in_the_pregnancies_column_by_outcome.webp
│   ├── 🖼️ distribution_of_patients_in_the_skin_thickness_column_by_outcome.webp
│   ├── 🖼️ exploring_the_age_feature.webp
│   ├── 🖼️ exploring_the_blood_pressure_feature.webp
│   ├── 🖼️ exploring_the_bmi_feature.webp
│   ├── 🖼️ exploring_the_diabetes_pedigree_function_feature.webp
│   ├── 🖼️ exploring_the_glucose_feature.webp
│   ├── 🖼️ exploring_the_insulin_feature.webp
│   ├── 🖼️ exploring_the_pregnancies_feature.webp
│   ├── 🖼️ exploring_the_skin_thickness_feature.webp
│   ├── 🖼️ feature_importance_heatmap_best_ml_model_xgbclassifier_recall_0_93.webp
│   ├── 🖼️ feature_importances_decisiontreeclassifier_recall_score_positive_class_0_925.webp
│   ├── 🖼️ feature_importances_logisticregression_recall_score_positive_class_0_9.webp
│   ├── 🖼️ feature_importances_randomforestclassifier_recall_score_positive_class_0_9.webp
│   ├── 🖼️ feature_importances_xgbclassifier_recall_score_positive_class_0_925.webp
│   ├── 🖼️ glucose_bin_vs_outcome_proportion.webp
│   ├── 🖼️ insulin_bin_vs_outcome_proportion.webp
│   ├── 🖼️ learning_curve_loss_class_weight.webp
│   ├── 🖼️ learning_curve_loss_class_weight_threshold.webp
│   ├── 🖼️ learning_curve_loss_dl_optuna.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_class_weight.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_class_weight_threshold.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_none.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_oversample.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_oversample_class_weight.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_oversample_class_weight_threshold.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_oversample_threshold.webp
│   ├── 🖼️ learning_curve_loss_feature_creation_threshold.webp
│   ├── 🖼️ learning_curve_loss_none.webp
│   ├── 🖼️ learning_curve_loss_oversample.webp
│   ├── 🖼️ learning_curve_loss_oversample_class_weight.webp
│   ├── 🖼️ learning_curve_loss_oversample_class_weight_threshold.webp
│   ├── 🖼️ learning_curve_loss_oversample_threshold.webp
│   ├── 🖼️ learning_curve_loss_threshold.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_class_weight.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_class_weight_threshold.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_dl_optuna.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_none.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_oversample.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_oversample_class_weight.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_oversample_class_weight_threshold.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_oversample_threshold.webp
│   ├── 🖼️ learning_curve_loss_with_feature_creation_threshold.webp
│   ├── 🖼️ learning_curve_loss_without_feature_creation_dl_optuna.webp
│   ├── 🖼️ model_leaderboard_for_models_with_feature_creation_recall_vs_precision_f1_size_accuracy_color.webp
│   ├── 🖼️ model_recall_performance_feature_creation_disabled.webp
│   ├── 🖼️ model_recall_performance_feature_creation_enabled.webp
│   ├── 🖼️ model_recall_ranking.webp
│   ├── 🖼️ multivariate_correlation_heatmap_numeric_columns.webp
│   ├── 🖼️ pairwise_cram_r_s_v_variables.webp
│   ├── 🖼️ pregnancies_bin_vs_outcome_proportion.webp
│   ├── 🖼️ roc_auc_comparison_across_models_with_feature_creation.webp
│   ├── 🖼️ shap_feature_importance_dl_optuna_with_feature_creation_recall_0_66.webp
│   ├── 🖼️ shap_feature_importance_dl_optuna_with_feature_creation_recall_0_76.webp
│   ├── 🖼️ shap_feature_importance_dl_optuna_with_feature_creation_recall_0_80.webp
│   ├── 🖼️ shap_feature_importance_dl_optuna_with_feature_creation_recall_0_83.webp
│   ├── 🖼️ shap_feature_importance_dl_optuna_with_feature_creation_recall_0_85.webp
│   ├── 🖼️ shap_value_distribution_per_feature_for_decisiontreeclassifier_recall_0_925.webp
│   ├── 🖼️ shap_value_distribution_per_feature_for_logisticregression_recall_0_900.webp
│   ├── 🖼️ shap_value_distribution_per_feature_for_randomforestclassifier_recall_0_850.webp
│   ├── 🖼️ shap_value_distribution_per_feature_for_randomforestclassifier_recall_0_900.webp
│   ├── 🖼️ shap_value_distribution_per_feature_for_xgbclassifier_recall_0_925.webp
│   ├── 🖼️ shap_value_distribution_per_feature_strip.webp
│   ├── 🖼️ skin_thickness_bin_vs_outcome_proportion.webp
│   ├── 🖼️ test_confusion_matrix_class_weight_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_class_weight_thr_0_14.webp
│   ├── 🖼️ test_confusion_matrix_class_weight_thr_0_26.webp
│   ├── 🖼️ test_confusion_matrix_class_weight_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_class_weight_threshold_thr_0_21.webp
│   ├── 🖼️ test_confusion_matrix_class_weight_threshold_thr_0_23.webp
│   ├── 🖼️ test_confusion_matrix_class_weight_threshold_thr_0_43.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_17.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_26.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_32.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_34.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_35.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_37.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_39.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_43.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_45.webp
│   ├── 🖼️ test_confusion_matrix_dl_optuna_thr_0_46.webp
│   ├── 🖼️ test_confusion_matrix_none_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_none_thr_0_12.webp
│   ├── 🖼️ test_confusion_matrix_none_thr_0_23.webp
│   ├── 🖼️ test_confusion_matrix_oversample_class_weight_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_oversample_class_weight_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_oversample_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_oversample_thr_0_34.webp
│   ├── 🖼️ test_confusion_matrix_oversample_thr_0_46.webp
│   ├── 🖼️ test_confusion_matrix_oversample_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_threshold_thr_0_28.webp
│   ├── 🖼️ test_confusion_matrix_threshold_thr_0_45.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_class_weight_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_class_weight_thr_0_23.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_class_weight_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_21.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_30.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_33.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_35.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_37.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_40.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_43.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_45.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_46.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_dl_optuna_thr_0_50.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_none_thr_0_30.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_none_thr_0_43.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_oversample_class_weight_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_oversample_class_weight_thr_0_41.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_oversample_class_weight_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_oversample_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_oversample_thr_0_39.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_oversample_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_with_feature_creation_threshold_thr_0_10.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_11.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_20.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_23.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_27.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_30.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_32.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_39.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_41.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_43.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_46.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_50.webp
│   ├── 🖼️ test_confusion_matrix_without_feature_creation_dl_optuna_thr_0_53.webp
│   └── 🖼️ top_feature_importances_decision_tree_diabetes_outcome_precision_0_510_recall_0_463.webp
├── 📁 reports
│   └── 📝 CriticalAnalysisEthics.md
├── 📝 LICENSE.md
└── 📝 README.md
```