"""
MedAI — Disease Prediction Engine
Random Forest Classifier trained on symptom-disease dataset.
Run `python ml/train.py` once to generate disease_predictor.pkl
"""
import os, pickle, numpy as np
from .symptoms_list import ALL_SYMPTOMS

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'disease_predictor.pkl')

_model = None

def _load_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
    return _model

SEVERITY_MAP = {
    'Flu': 'Low', 'Common Cold': 'Low', 'Migraine': 'Medium',
    'Dengue': 'High', 'Malaria': 'High', 'Typhoid': 'High',
    'Diabetes': 'Medium', 'Hypertension': 'Medium', 'Pneumonia': 'High',
    'Allergy': 'Low', 'Gastroenteritis': 'Medium', 'Arthritis': 'Medium',
    'Asthma': 'Medium', 'Jaundice': 'High', 'Tuberculosis': 'High',
    'Urinary Tract Infection': 'Medium', 'Chicken Pox': 'Low',
    'Heart Disease': 'High', 'Anemia': 'Medium', 'Psoriasis': 'Low',
}

def symptoms_to_vector(text: str) -> np.ndarray:
    text_lower = text.lower()
    vec = np.zeros(len(ALL_SYMPTOMS), dtype=int)
    for i, sym in enumerate(ALL_SYMPTOMS):
        if sym.lower() in text_lower:
            vec[i] = 1
    return vec

def predict_disease(symptoms_text: str):
    model = _load_model()
    if model is None:
        # Fallback rule-based prediction when model not trained yet
        return _rule_based(symptoms_text)

    vec = symptoms_to_vector(symptoms_text).reshape(1, -1)
    proba = model.predict_proba(vec)[0]
    classes = model.classes_
    top_idx = np.argsort(proba)[::-1][:3]
    results = []
    for idx in top_idx:
        disease = classes[idx]
        conf = round(float(proba[idx]) * 100, 1)
        if conf < 1:
            continue
        results.append({
            'disease': disease,
            'confidence': conf,
            'severity': SEVERITY_MAP.get(disease, 'Medium'),
        })
    return results if results else _rule_based(symptoms_text)

# ── Rule-based fallback ──────────────────────────────────────────────────────

RULES = [
    (['fever', 'cough', 'fatigue', 'body ache'],          'Flu',           88.0),
    (['fever', 'rash', 'joint pain', 'headache'],         'Dengue',        82.0),
    (['fever', 'chills', 'sweating', 'vomiting'],         'Malaria',       79.0),
    (['sneezing', 'runny nose', 'sore throat'],           'Common Cold',   91.0),
    (['headache', 'nausea', 'light sensitivity'],         'Migraine',      85.0),
    (['chest pain', 'shortness of breath', 'dizziness'], 'Heart Disease', 75.0),
    (['frequent urination', 'thirst', 'fatigue'],         'Diabetes',      80.0),
    (['high bp', 'headache', 'blurred vision'],           'Hypertension',  78.0),
    (['cough', 'mucus', 'chest congestion', 'fever'],     'Pneumonia',     83.0),
    (['itching', 'skin rash', 'watery eyes'],             'Allergy',       87.0),
    (['diarrhea', 'vomiting', 'stomach pain'],            'Gastroenteritis', 84.0),
    (['yellow skin', 'dark urine', 'fatigue'],            'Jaundice',      81.0),
    (['burning urination', 'frequent urination'],         'Urinary Tract Infection', 86.0),
    (['joint pain', 'swelling', 'stiffness'],             'Arthritis',     77.0),
    (['wheezing', 'shortness of breath', 'chest tightness'], 'Asthma',    82.0),
]

OTHERS = [
    ('Chicken Pox',   72.0, 'Low'),
    ('Tuberculosis',  65.0, 'High'),
    ('Anemia',        60.0, 'Medium'),
]

def _rule_based(text: str):
    text_lower = text.lower()
    scored = []
    for keywords, disease, base_conf in RULES:
        hits = sum(1 for k in keywords if k in text_lower)
        if hits > 0:
            conf = round(base_conf * hits / len(keywords), 1)
            scored.append((conf, disease))
    scored.sort(reverse=True)
    results = []
    for conf, disease in scored[:3]:
        results.append({
            'disease': disease,
            'confidence': conf,
            'severity': SEVERITY_MAP.get(disease, 'Medium'),
        })
    # Pad with others if needed
    for disease, conf, sev in OTHERS:
        if len(results) >= 3:
            break
        if not any(r['disease'] == disease for r in results):
            results.append({'disease': disease, 'confidence': conf, 'severity': sev})
    if not results:
        results = [
            {'disease': 'Flu',         'confidence': 65.0, 'severity': 'Low'},
            {'disease': 'Common Cold', 'confidence': 55.0, 'severity': 'Low'},
            {'disease': 'Allergy',     'confidence': 40.0, 'severity': 'Low'},
        ]
    return results
