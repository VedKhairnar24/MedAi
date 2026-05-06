"""
MedAI — Train Random Forest Model
Run once:  python ml/train.py
Generates: ml/disease_predictor.pkl
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from ml.symptoms_list import ALL_SYMPTOMS

# ── Load Dataset from CSV ───────────────────────────────────────────────────

def load_dataset():
    """Load training data from MedAi_dataset.csv"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'MedAi_dataset.csv')
    df = pd.read_csv(csv_path)
    
    dataset = []
    for _, row in df.iterrows():
        # Parse symptoms (remove extra spaces and filter empty strings)
        symptoms = [s.strip() for s in row['Symptoms'].split(',') if s.strip()]
        disease = row['Disease'].strip()
        dataset.append((symptoms, disease))
    
    return dataset

DATASET = load_dataset()

def row_to_vector(symptoms):
    vec = np.zeros(len(ALL_SYMPTOMS), dtype=int)
    for sym in symptoms:
        if sym in ALL_SYMPTOMS:
            vec[ALL_SYMPTOMS.index(sym)] = 1
    return vec

def main():
    X, y = [], []
    # Augment with slight noise
    for syms, disease in DATASET:
        for _ in range(10):
            vec = row_to_vector(syms).copy()
            # Random drop 1 symptom
            ones = np.where(vec == 1)[0]
            if len(ones) > 1:
                drop = np.random.choice(ones)
                vec[drop] = 0
            X.append(vec)
            y.append(disease)

    X, y = np.array(X), np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)

    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"✅  Model accuracy: {acc*100:.1f}%")

    out_path = os.path.join(os.path.dirname(__file__), 'disease_predictor.pkl')
    with open(out_path, 'wb') as f:
        pickle.dump(clf, f)
    print(f"💾  Model saved to {out_path}")

if __name__ == '__main__':
    main()
