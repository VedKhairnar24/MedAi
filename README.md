# 🏥 MedAI — Intelligent Doctor Consultation & Symptom Analysis Assistant

> **For Educational Purposes Only — Not a Medical Substitute**

## Tech Stack
- **Backend:** Python 3.x + Flask
- **AI/ML:** scikit-learn (Random Forest), pandas, numpy
- **Database:** SQLite (dev) / MySQL (production)
- **Frontend:** HTML5, Bootstrap 5, Jinja2, Vanilla JS

---

## 🚀 Setup Instructions

### 1. Clone / Extract the project
```bash
cd medai/
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the ML model (one-time)
```bash
python ml/train.py
# Output: ml/disease_predictor.pkl  (~85%+ accuracy)
```

### 5. Run the application
```bash
python app.py
```

### 6. Open in browser
```
http://localhost:5000
```

---

## 👤 Default Login Credentials

| Role    | Email                  | Password     |
|---------|------------------------|--------------|
| Admin   | admin@medai.com        | admin123     |
| Doctor  | priya@medai.com        | Doctor@123   |
| Doctor  | rahul@medai.com        | Doctor@123   |
| Doctor  | sneha@medai.com        | Doctor@123   |

---

## 📁 Project Structure

```
medai/
├── app.py                  # Main Flask application
├── requirements.txt
├── ml/
│   ├── __init__.py
│   ├── predictor.py        # Disease prediction engine
│   ├── chatbot.py          # AI chatbot responses
│   ├── symptoms_list.py    # Feature symptom list
│   ├── train.py            # Model training script
│   └── disease_predictor.pkl  (generated after training)
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── predict.html        # Symptom checker
    ├── appointments.html
    ├── chatbot.html
    ├── history.html
    ├── doctor.html
    └── admin.html
```

---

## 🧠 ML Prediction Engine

- **Algorithm:** Random Forest Classifier (100–200 estimators)
- **Input:** Binary symptom vector (1 = present, 0 = absent)
- **Output:** Top 3 diseases with confidence scores
- **Training split:** 80% train / 20% test
- **Target accuracy:** 85%+
- **Model file:** `ml/disease_predictor.pkl` (pickle)

### Diseases Covered (20+)
Flu, Common Cold, Dengue, Malaria, Typhoid, Migraine, Diabetes, Hypertension,
Pneumonia, Allergy, Gastroenteritis, Arthritis, Asthma, Jaundice, Tuberculosis,
Urinary Tract Infection, Chicken Pox, Heart Disease, Anemia, Psoriasis

---

## 🔐 User Roles

| Role    | Capabilities |
|---------|-------------|
| Patient | Symptom check, appointments, chatbot, health history |
| Doctor  | View & manage own appointments |
| Admin   | Full system: user management, add doctors, analytics |

---

## 📊 Database Schema (SQLite / MySQL)

- **users** — id, name, email, password (hashed), role, created_at
- **symptoms_history** — id, user_id (FK), symptoms, predicted_disease, confidence_score, severity, created_at
- **doctors** — doctor_id, name, specialization, available_slots (JSON), user_id (FK)
- **appointments** — appointment_id, user_id (FK), doctor_id (FK), date, time_slot, status

---

## 🔮 Future Scope

- 🎙 Voice input (Speech-to-Text)
- 🌐 Multilingual support (Hindi, Marathi, Tamil)
- 📷 Skin disease detection (CNN)
- 💊 Medicine reminders via SMS/Email
- ⌚ Wearable device sync
- 📹 Telemedicine (WebRTC video calls)

---

## ⚠️ Disclaimer

MedAI is built for **academic/educational purposes**. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

*Academic Year: 2024–25 | Mini Project Submission*
