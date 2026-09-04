import pickle
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
with (BASE_DIR / "models" / "event_model.pkl").open("rb") as f:
    model = pickle.load(f)
with (BASE_DIR / "models" / "risk_maps.pkl").open("rb") as f:
    risk_maps = pickle.load(f)

zone_risk_map = risk_maps["zone_risk"]
cause_risk_map = risk_maps["cause_risk"]
hour_risk_map = risk_maps["hour_risk"]

MODEL_FEATURES = [
    "event_type","event_cause","zone","requires_road_closure",
    "hour","weekday","zone_risk","cause_risk","hour_risk"
]

def _average(mapping):
    return sum(mapping.values()) / len(mapping) if mapping else 0.0

def predict_priority(event_type, event_cause, zone, requires_road_closure, hour, weekday):
    input_df = pd.DataFrame([{
        "event_type": event_type,
        "event_cause": event_cause,
        "zone": zone,
        "requires_road_closure": bool(requires_road_closure),
        "hour": int(hour),
        "weekday": weekday,
        "zone_risk": zone_risk_map.get(zone, _average(zone_risk_map)),
        "cause_risk": cause_risk_map.get(event_cause, _average(cause_risk_map)),
        "hour_risk": hour_risk_map.get(float(hour), _average(hour_risk_map)),
    }], columns=MODEL_FEATURES)
    prediction = int(model.predict(input_df)[0])
    probabilities = model.predict_proba(input_df)[0]
    confidence = float(probabilities[prediction])
    return ("High" if prediction == 1 else "Low"), confidence
