# **Chapter 5 — Critical Analysis, Ethics & Governance**

As I developed and evaluated the machine learning and deep learning models in this project, I became increasingly aware that technical performance alone is not enough to justify clinical use. Any model intended for healthcare must also be examined through ethical, clinical, and governance lenses. In this chapter, I reflect on the rationale behind my metric choices, compare the behavior of different model families, assess fairness risks, and outline why further validation is essential before considering real‑world deployment.

---

## **5.1 Prioritizing Recall Over Accuracy in Healthcare**

Throughout this project, I deliberately prioritized **recall** rather than accuracy. In diabetes screening, the ethical priority is to **avoid false negatives**—patients who genuinely have elevated risk but are incorrectly classified as low‑risk. Missing these individuals can delay diagnosis and treatment, increasing the likelihood of long‑term complications such as neuropathy, retinopathy, and cardiovascular disease.

Accuracy, although commonly reported, can be misleading in imbalanced datasets. A model may achieve high accuracy simply by predicting the majority class while still failing to identify a meaningful proportion of true positives. By contrast, recall directly measures the model’s ability to capture high‑risk patients.

My results reinforced this decision. With feature creation, several models achieved recall values between **0.90 and 0.93**, outperforming established screening tools such as the ADA Prediabetes Risk Test, which demonstrated **78.9% sensitivity** in a Saudi population (Aldayel et al., 2021). Prioritizing recall allowed me to align the model’s behavior with clinical safety standards and reduce the risk of underdiagnosis.

---

## **5.2 Comparing Machine Learning and Deep Learning Performance**

### **5.2.1 Generalization on Tabular Clinical Data**

As I compared model families, I observed a consistent pattern: **traditional machine learning models generalized better than deep learning models** on this structured clinical dataset. XGBoost and Random Forests, in particular, delivered the strongest recall and the most stable performance across resampling strategies.

This aligns with published evidence showing that deep neural networks often struggle with tabular data unless supported by large datasets or sophisticated representation learning. In contrast, tree‑based models naturally capture nonlinear interactions and handle missingness more effectively.

### **5.2.2 Impact of Feature Creation**

Feature creation had a substantial impact on performance:

- **Without feature creation:** recall = 0.85–0.90  
- **With feature creation:** recall = 0.90–0.93  

The uplift was especially pronounced for XGBoost and Random Forests. By introducing clinically meaningful interactions—such as glucose×BMI, age×DPF, and pregnancies×glucose—I enabled the models to learn relationships that deep learning models did not automatically discover from raw inputs.

### **5.2.3 Stability and Interpretability**

I also found that machine learning models offered:

- more stable performance under different resampling strategies  
- clearer interpretability through feature importance  
- reduced sensitivity to small dataset sizes  

These characteristics make ML models more suitable for early‑stage clinical decision support, where transparency and reliability are essential.

---

## **5.3 Dataset Bias and Fairness Considerations**

### **5.3.1 Sources of Bias**

While analyzing the dataset, I recognized several potential sources of bias. Clinical datasets often reflect structural inequities in healthcare access, diagnostic frequency, and demographic representation. Bias may arise from:

- underrepresentation of certain demographic groups  
- missingness patterns linked to socioeconomic status  
- sampling from a single geographic region  
- historical disparities in diagnostic coding  

These factors can lead to uneven model performance across subgroups.

### **5.3.2 Fairness Risks**

If left unaddressed, such biases may cause the model to:

- underperform for minority or underserved populations  
- overpredict risk for specific demographic groups  
- reinforce existing healthcare disparities  

Given the ethical implications, fairness must be evaluated as rigorously as accuracy or recall.

### **5.3.3 Mitigation Strategies**

To mitigate these risks, I plan to incorporate:

- subgroup performance analysis (e.g., recall by age, gender, ethnicity)  
- bias‑aware resampling or reweighting  
- continuous monitoring for performance drift  
- transparent reporting of limitations  

Fairness is not a one‑time task but an ongoing governance requirement.

---

## **5.4 Limitations and the Need for Further Clinical Validation**

Despite the strong performance of the models, I recognize several limitations that must be addressed before considering clinical deployment.

### **5.4.1 Dataset Size and Representativeness**

The dataset is relatively small and may not capture rare clinical patterns or population‑level variability. External validation on independent cohorts is essential to ensure generalizability.

### **5.4.2 Single‑Site Data**

Because the data originates from a single region, the models may not generalize to other clinical environments with different demographics, diagnostic practices, or measurement protocols.

### **5.4.3 Temporal Drift**

Clinical populations evolve over time. Without ongoing monitoring, model performance may degrade as disease prevalence, diagnostic criteria, or patient behavior shifts.

### **5.4.4 Precision–Recall Tradeoff**

Although high recall is clinically desirable, it comes with increased false positives. This may burden clinical workflows, so thresholds must be calibrated to balance sensitivity with operational feasibility.

### **5.4.5 Explainability and Clinical Trust**

While SHAP improves interpretability, clinicians must be trained to understand and contextualize model explanations. AI systems should support—not replace—clinical judgment.

---

## **5.5 Governance Requirements for Safe Deployment**

Before any real‑world use, I would need to implement a comprehensive governance framework that includes:

- **External validation** on a geographically distinct cohort  
- **Prospective testing** to evaluate real‑world performance  
- **Calibration monitoring** to ensure probability reliability  
- **Bias and fairness audits** across demographic subgroups  
- **Human‑in‑the‑loop oversight**, ensuring clinicians retain final decision authority  
- **Complete documentation** of data sources, preprocessing, model versions, and threshold selection  

These steps align with international AI governance frameworks (WHO, OECD, EU AI Act) and ensure that the system is safe, transparent, and clinically responsible.

---

## **Conclusion**

Through this project, I demonstrated that machine learning models—especially when enhanced with feature creation—can achieve clinically meaningful sensitivity for diabetes risk prediction. However, technical performance alone is not sufficient for clinical deployment. Ethical considerations, fairness assessments, and robust governance mechanisms are essential to ensure that the model supports early detection while safeguarding patient welfare. With these safeguards in place, the system has the potential to contribute meaningfully to improved clinical outcomes.
