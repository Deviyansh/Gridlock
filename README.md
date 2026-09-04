# 🚦 Gridlock — Traffic Intelligence Platform

Gridlock is a unified traffic-intelligence portfolio project combining two complementary components from the original Gridlock repositories:

- **Incident Intelligence:** predicts traffic-incident priority and generates response recommendations.
- **Demand Analytics:** preserves and visualizes the competition traffic-demand modelling work and its submission output.

The application is demonstrated using anonymized Bengaluru traffic-event data.

## Live Application

**Live Deployment**- https://gridlock-traffic-intelligence.onrender.com/

## Features

### 🧠 Incident Intelligence
- CatBoost-based High/Low incident-priority prediction
- Event type, cause, zone, road-closure, hour, and weekday inputs
- Risk-map feature enrichment
- Confidence score and severity assessment
- Response-team recommendations
- Traffic-officer and barricade allocation
- Road-closure diversion actions

### 📈 Demand Analytics
- Preserved traffic-demand prediction research notebook
- 77,299 training rows and 41,778 test rows documented in the original notebook
- Temporal and geospatial feature engineering
- CatBoost V1/V2/V3 experiments
- LightGBM and ensemble exploration
- Hyperparameter search
- Preserved submission output and model-comparison results

> The original demand repository did not include the source `train.csv` / `test.csv` files or a serialized trained demand model. Therefore this module is presented as analysis of the preserved competition output rather than as a new interactive demand predictor.

## Machine Learning

### Incident Priority Model

**Model:** CatBoostClassifier

**Target:** Priority (`Low` / `High`)

**Features:**
- `event_type`
- `event_cause`
- `zone`
- `requires_road_closure`
- `hour`
- `weekday`
- `zone_risk`
- `cause_risk`
- `hour_risk`

The trained model and risk maps are included under `models/`.

### Traffic Demand Research

The original demand-prediction notebook evaluates CatBoost and LightGBM approaches using geospatial, temporal, road-infrastructure, and environmental features, plus historical geohash statistics and early Day-49 signals.

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- CatBoost
- Folium
- Plotly
- Jupyter Notebook

## Project Structure

```text
Gridlock-Integrated/
├── app.py
├── app/
│   ├── dashboard.py
│   ├── predictor.py
│   └── recommender.py
├── data/
│   └── Astram event data anonymized.csv
├── models/
│   ├── event_model.pkl
│   └── risk_maps.pkl
├── notebooks/
│   ├── event_analysis.ipynb
│   ├── model.ipynb
│   └── demand_prediction/
│       └── model_v1_final.ipynb
├── outputs/
│   ├── model_comparison.csv
│   └── submission_v1.csv
├── render.yaml
├── requirements.txt
└── README.md
```

## Run Locally

```bash
git clone <your-repository-url>
cd Gridlock-Integrated

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deployment

The project includes `render.yaml` for deployment as a Streamlit web service on Render.

Add the actual public URL to the **Live Application** section after deployment.

## Use Cases

- Traffic operations support
- Incident prioritization
- Emergency-response planning
- Urban mobility analysis
- Smart-city analytics
- Traffic-demand research

## Limitations

- The incident model is a decision-support prototype and should not autonomously control traffic infrastructure.
- The demand-model training data and serialized model were not present in the original repository, so that module cannot honestly be presented as a retrainable live predictor without those assets.
- Historical dashboards and recommendations should be interpreted in the context of the supplied anonymized data.
