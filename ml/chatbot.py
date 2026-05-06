"""MedAI Chatbot — rule-based + keyword health guidance."""

EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', 'stroke', 'unconscious', 'not breathing',
    'severe bleeding', 'seizure', 'overdose', 'choking',
]

FAQ = {
    'appointment': 'You can book an appointment from the Appointments section. Choose a doctor and available slot.',
    'history': 'Your past consultations are saved under the Health History section.',
    'accuracy': 'Our ML model targets 85%+ accuracy. However, it is for guidance only — always consult a real doctor.',
    'emergency': '🚨 Please call emergency services (112) immediately or visit the nearest hospital!',
    'fever': 'For fever: rest, drink plenty of fluids, take paracetamol if needed. See a doctor if it persists > 3 days or goes above 104°F.',
    'cold': 'Common cold usually resolves in 7–10 days. Rest, stay hydrated, use steam inhalation.',
    'headache': 'Headache can have many causes. Drink water, rest in a dark room. If severe or sudden, seek medical help.',
    'diabetes': 'Monitor blood sugar regularly, follow a low-sugar diet, take prescribed medication, and exercise daily.',
    'bp': 'For high blood pressure: reduce salt, exercise, manage stress, avoid smoking & alcohol.',
    'covid': 'COVID symptoms include fever, cough, fatigue, and loss of smell/taste. Isolate and get tested.',
    'vaccine': 'Stay up to date with vaccinations. Consult your doctor for the recommended schedule.',
    'diet': 'Eat a balanced diet with fruits, vegetables, whole grains, lean protein, and low sugar/salt.',
    'exercise': 'Aim for at least 30 minutes of moderate exercise 5 days a week.',
    'sleep': 'Adults need 7–9 hours of sleep. Good sleep improves immunity, mood, and cognitive function.',
    'stress': 'Manage stress with meditation, deep breathing, exercise, and talking to someone you trust.',
}

GREETINGS = ['hello', 'hi', 'hey', 'good morning', 'good evening', 'namaste']

def chatbot_response(message: str) -> str:
    msg = message.lower().strip()

    # Emergency check
    for kw in EMERGENCY_KEYWORDS:
        if kw in msg:
            return ('🚨 <strong>Emergency detected!</strong> Please call <strong>112</strong> or go to the nearest emergency room immediately. '
                    'Do not wait for an online consultation.')

    # Greetings
    if any(g in msg for g in GREETINGS):
        return ('👋 Hello! I\'m MedAI\'s health assistant. I can help you with:<br>'
                '• Symptom guidance<br>• Appointment info<br>• Health tips<br>'
                'Type your health question below!')

    # FAQ keyword matching
    for key, answer in FAQ.items():
        if key in msg:
            return answer

    # Symptom-based guidance
    if any(w in msg for w in ['symptom', 'feeling', 'pain', 'ache', 'sick', 'ill', 'suffer']):
        return ('Please use our <strong>Symptom Checker</strong> tool for a detailed AI-powered prediction. '
                'Describe your symptoms clearly for best results. Remember, this is for guidance only — '
                'consult a doctor for diagnosis.')

    if 'doctor' in msg or 'specialist' in msg:
        return 'You can find and book available doctors in the <strong>Appointments</strong> section.'

    if 'report' in msg or 'pdf' in msg:
        return 'Your consultation reports are available in the <strong>Health History</strong> section. You can download them as PDF.'

    if 'medai' in msg or 'about' in msg:
        return ('MedAI is an AI-powered health assistant that predicts diseases from symptoms using Random Forest ML, '
                'offers doctor appointment booking, and maintains your health history — all in one platform.')

    return ('I\'m not sure about that. You can ask me about symptoms, appointments, health tips, or how MedAI works. '
            'For medical emergencies, please call <strong>112</strong>.')
