from pathlib import Path
import pandas as pd
import streamlit as st

from app.predictor import predict_priority
from app.recommender import generate_recommendation

BASE_DIR = Path(__file__).resolve().parent.parent
EVENT_DATA = BASE_DIR / "data" / "Astram event data anonymized.csv"
DEMAND_SUBMISSION = BASE_DIR / "outputs" / "submission_v1.csv"
COMPARISON = BASE_DIR / "outputs" / "model_comparison.csv"

st.set_page_config(page_title="Gridlock | Traffic Intelligence", page_icon="🚦", layout="wide")

@st.cache_data
def load_events():
    df = pd.read_csv(EVENT_DATA)
    df["start_datetime"] = pd.to_datetime(df["start_datetime"], errors="coerce")
    return df

@st.cache_data
def load_demand():
    return pd.read_csv(DEMAND_SUBMISSION)

events, demand = load_events(), load_demand()

st.sidebar.title("🚦 Gridlock")
st.sidebar.caption("AI-powered traffic intelligence platform")
page = st.sidebar.radio("Navigate", ["Command Center","Incident Intelligence","Demand Analytics","About"])

if page == "Command Center":
    st.title("🚦 Gridlock Traffic Intelligence")
    st.write("Unified traffic incident decision support and demand analytics for smart-city operations.")
    total = len(events)
    high = int((events["priority"].fillna("") == "High").sum())
    closures = int(events["requires_road_closure"].fillna(False).sum())
    peak = int(events["start_datetime"].dt.hour.mode().iloc[0]) if events["start_datetime"].notna().any() else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Recorded Events", f"{total:,}")
    c2.metric("High-Priority Events", f"{high:,}")
    c3.metric("Road Closures", f"{closures:,}")
    c4.metric("Most Common Hour", f"{peak:02d}:00")

    st.markdown("---")
    a,b=st.columns(2)
    with a: st.info("### 🧠 Incident Intelligence\nPredict incident priority and generate an operational response plan.")
    with b: st.info("### 📈 Demand Analytics\nExplore the preserved traffic-demand modelling results and submission output.")

    left,right=st.columns(2)
    with left:
        st.subheader("Event Causes")
        st.bar_chart(events["event_cause"].fillna("Unknown").value_counts().head(8))
    with right:
        st.subheader("Priority Distribution")
        st.bar_chart(events["priority"].fillna("Unknown").value_counts())

elif page == "Incident Intelligence":
    st.title("🧠 Incident Intelligence")
    st.caption("CatBoost-based incident prioritization with response recommendations.")
    event_type=st.selectbox("Event Type",["planned","unplanned"])
    event_cause=st.selectbox("Event Cause",sorted(events["event_cause"].dropna().astype(str).unique()))
    zone=st.selectbox("Zone",sorted(events["zone"].dropna().astype(str).unique()))
    closure=st.checkbox("Requires Road Closure")
    hour=st.slider("Hour of occurrence",0,23,12)
    weekday=st.selectbox("Weekday",["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

    if st.button("Analyze Incident", type="primary", use_container_width=True):
        priority, confidence=predict_priority(event_type,event_cause,zone,closure,hour,weekday)
        rec=generate_recommendation(priority,event_cause,zone,closure)
        score=round(confidence*100)
        label="Critical" if score>=80 else "High" if score>=60 else "Medium" if score>=40 else "Low"

        st.markdown("---")
        k1,k2,k3=st.columns(3)
        k1.metric("Predicted Priority",priority)
        k2.metric("Model Confidence",f"{confidence*100:.1f}%")
        k3.metric("Alert Level",rec["alert_level"])

        st.subheader("⚠️ Severity Assessment")
        st.progress(confidence)
        st.write(f"Severity score: **{score}/100** — {label} risk")

        r1,r2=st.columns(2)
        r1.metric("Traffic Officers",rec["officers"])
        r2.metric("Barricades",rec["barricades"])
        st.info(f"Impact category: **{rec['impact_category']}**")

        l,r=st.columns(2)
        with l:
            st.subheader("👮 Response Team")
            for x in rec["response_team"]: st.write(f"• {x}")
        with r:
            st.subheader("✅ Recommended Actions")
            for x in rec["recommended_actions"]: st.write(f"• {x}")

        st.subheader("🧠 Prediction Signals")
        reasons=[]
        if closure: reasons.append("Road closure is required.")
        if event_type=="unplanned": reasons.append("The incident is unplanned.")
        if event_cause in {"accident","vehicle_breakdown","construction"}: reasons.append(f"Event cause is {event_cause.replace('_',' ')}.")
        if hour in [7,8,9,17,18,19,20]: reasons.append("Occurrence falls in a common peak-traffic window.")
        if not reasons: reasons.append("No additional rule-based escalation signal was triggered.")
        for x in reasons: st.write(f"• {x}")

elif page == "Demand Analytics":
    st.title("📈 Traffic Demand Analytics")
    st.caption("Preserved analysis of the competition traffic-demand prediction output.")
    c1,c2,c3=st.columns(3)
    c1.metric("Prediction Rows",f"{len(demand):,}")
    c2.metric("Mean Demand",f"{demand['demand'].mean():.4f}")
    c3.metric("Max Demand",f"{demand['demand'].max():.4f}")
    st.subheader("Demand Distribution")
    st.bar_chart(demand["demand"].round(2).value_counts().sort_index())
    st.subheader("Highest Predicted-Demand Records")
    st.dataframe(demand.sort_values("demand",ascending=False).head(20),use_container_width=True,hide_index=True)
    if COMPARISON.exists():
        st.subheader("Model Comparison")
        st.dataframe(pd.read_csv(COMPARISON),use_container_width=True,hide_index=True)
    st.info("The original demand repository contains the modelling notebook and submission output, but not the source train/test datasets or a serialized demand model. This module therefore presents the preserved competition output rather than claiming an interactive retrainable predictor.")

else:
    st.title("ℹ️ About Gridlock")
    st.write("Gridlock combines the original traffic-demand modelling work and the incident-management prototype into one portfolio application.")
    st.subheader("Machine Learning")
    st.markdown("- **Incident Intelligence:** CatBoostClassifier for High/Low incident priority.\n- **Demand Research:** CatBoostRegressor experiments with temporal, geospatial, road, and environmental features.")
    st.subheader("Included Assets")
    st.markdown("- Anonymized Bengaluru traffic-event dataset\n- Trained incident model and risk maps\n- Demand modelling notebook and competition outputs")
    st.warning("Gridlock is a research and decision-support prototype. Predictions should not autonomously control traffic infrastructure.")

st.markdown("---")
st.caption("@Noctis")
