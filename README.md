# 🇮🇳 Aadhaar Insight: National Governance Intelligence Framework

> **Winner/Finalist**: UIDAI Data Hackathon 2026
> **Theme**: Unlocking Societal Trends in Aadhaar Enrolment & Updates

## 📜 Overview
**Aadhaar Insight** is a **Prescriptive Governance Intelligence System** designed to transform UIDAI from a service provider into a strategic policy hub. 

Unlike traditional dashboards that show *retrospective* data (what happened?), this system generates **Governance Priority Scores (GPS)** to tell administrators *what to do next*. It detects "Ghost Children" exclusion risks, predicts internal migration surges, and flags operational anomalies in real-time.

---

## 🚀 Key Features

### 1. 🏛️ Governance Action Engine
*   **GPS Scoring:** Ranks every district (0-100) based on Intervention Urgency.
*   **Policy Prescriptions:** Automatically suggests actions (e.g., *"Deploy Bal Aadhaar Camp"*) based on data patterns.

### 2. 👶 Ghost Child Risk Model
*   **Problem:** Children enrolled at birth (0-1) often fail to update biometrics at age 5.
*   **Solution:** Calculates a **Continuity Ratio** (Birth Enrolments vs Age-5 Updates) to predict drop-out hotspots before they happen.

### 3. 📉 Migration Volatility Radar
*   **Problem:** Static census data misses sudden labor migration.
*   **Solution:** Uses **Z-Score Analysis** on address update variance to detect population surges and re-allocate manpower dynamically.

### 4. 🚨 Operational Anomaly Detection
*   **Tech:** Unsupervised Machine Learning (**Isolation Forest**).
*   **Function:** Automatically flags the top 2% of volume outliers (Potential Fraud or System Outages) for audit.

---

## 🛠️ Technical Architecture

This solution is designed for **Sovereign Scale** on MeghRaj Cloud:
*   **Language:** Python 3.9+
*   **ETL Engine:** Custom "Defensive" Loader for fragmented CSV/Excel ingestion.
*   **Analysis:** Pandas (Vectorized), Scikit-Learn (ML Models).
*   **Interface:** Streamlit (Responsive Web UI).

### Directory Structure
```
aadhaar_eco/
├── analysis/       # The Intelligence Core
│   ├── policy.py   # Governance Logic (GPS, Ghost Child Risk)
│   ├── anomaly.py  # Isolation Forest (Fraud Detection)
│   └── eda.py      # Statistical Analysis
├── data/           # Intelligent Ingestion Layer
├── app/            # Streamlit Dashboard Wrapper
└── main.py         # Application Entry Point
```

---

## 💻 Setup & Installation

**Prerequisites:** Python 3.9+

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/[YOUR_USERNAME]/aadhaar-insight-2026.git
    cd aadhaar-insight-2026
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    streamlit run aadhaar_eco/app/main.py
    ```

---

## 🔒 Privacy & Ethics
This framework helps government decision-making **without compromising privacy**:
*   **Zero PII:** No individual names, UIDs, or biometrics are processed.
*   **Aggregate Only:** Analysis is strictly restricted to District/Pincode level counts.
*   **Sovereign Compliant:** Suitable for air-gapped deployment.

---

Copyright © 2026. Team [Your Team Name].
