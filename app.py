from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pickle, os, json
from ml.predictor import predict_disease
from ml.chatbot import chatbot_response

app = Flask(__name__)
app.secret_key = 'medai_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── Models ──────────────────────────────────────────────────────────────────

class User(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    email       = db.Column(db.String(150), unique=True, nullable=False)
    password    = db.Column(db.String(200), nullable=False)
    role        = db.Column(db.String(20), default='patient')  # patient | doctor | admin
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

class SymptomsHistory(db.Model):
    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symptoms          = db.Column(db.Text, nullable=False)
    predicted_disease = db.Column(db.String(200))
    confidence_score  = db.Column(db.Float)
    severity          = db.Column(db.String(20))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

class Doctor(db.Model):
    doctor_id        = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(100), nullable=False)
    specialization   = db.Column(db.String(100))
    available_slots  = db.Column(db.Text)          # JSON list of slots
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'))

class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id      = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'), nullable=False)
    date           = db.Column(db.String(20))
    time_slot      = db.Column(db.String(30))
    status         = db.Column(db.String(20), default='Pending')

# ── Auth ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = generate_password_hash(request.form['password'])
        role     = request.form.get('role', 'patient')
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            return redirect(url_for('patient_dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── Patient ──────────────────────────────────────────────────────────────────

@app.route('/dashboard')
def patient_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    history = SymptomsHistory.query.filter_by(user_id=session['user_id'])\
                                   .order_by(SymptomsHistory.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', history=history)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    results = None
    if request.method == 'POST':
        symptoms_text = request.form.get('symptoms', '')
        results = predict_disease(symptoms_text)
        if results:
            top = results[0]
            record = SymptomsHistory(
                user_id=session['user_id'],
                symptoms=symptoms_text,
                predicted_disease=top['disease'],
                confidence_score=top['confidence'],
                severity=top['severity'],
            )
            db.session.add(record)
            db.session.commit()
    return render_template('predict.html', results=results, enumerate=enumerate)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    records = SymptomsHistory.query.filter_by(user_id=session['user_id'])\
                                   .order_by(SymptomsHistory.created_at.desc()).all()
    return render_template('history.html', records=records)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doctors = Doctor.query.all()
    if request.method == 'POST':
        appt = Appointment(
            user_id=session['user_id'],
            doctor_id=int(request.form['doctor_id']),
            date=request.form['date'],
            time_slot=request.form['time_slot'],
        )
        db.session.add(appt)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('appointments'))
    my_appts = Appointment.query.filter_by(user_id=session['user_id']).all()
    return render_template('appointments.html', doctors=doctors, my_appts=my_appts)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    msg  = data.get('message', '')
    reply = chatbot_response(msg)
    return jsonify({'reply': reply})

# ── Doctor ───────────────────────────────────────────────────────────────────

@app.route('/doctor')
def doctor_dashboard():
    if session.get('role') != 'doctor':
        return redirect(url_for('login'))
    doc = Doctor.query.filter_by(user_id=session['user_id']).first()
    if not doc:
        return render_template('doctor.html', appts=[])
    appts = Appointment.query.filter_by(doctor_id=doc.doctor_id).all()
    return render_template('doctor.html', appts=appts)

@app.route('/doctor/update/<int:appt_id>/<status>')
def update_appt(appt_id, status):
    if session.get('role') not in ('doctor', 'admin'):
        return redirect(url_for('login'))
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = status
    db.session.commit()
    return redirect(request.referrer or url_for('doctor_dashboard'))

# ── Admin ────────────────────────────────────────────────────────────────────

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    users    = User.query.all()
    doctors  = Doctor.query.all()
    appts    = Appointment.query.all()
    records  = SymptomsHistory.query.all()
    return render_template('admin.html', users=users, doctors=doctors,
                           appts=appts, records=records)

@app.route('/admin/add_doctor', methods=['POST'])
def add_doctor():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    name   = request.form['name']
    spec   = request.form['specialization']
    slots  = json.dumps(['09:00', '10:00', '11:00', '14:00', '15:00', '16:00'])
    # Create a user account for the doctor
    email    = request.form['email']
    password = generate_password_hash('Doctor@123')
    u = User(name=name, email=email, password=password, role='doctor')
    db.session.add(u)
    db.session.flush()
    doc = Doctor(name=name, specialization=spec, available_slots=slots, user_id=u.id)
    db.session.add(doc)
    db.session.commit()
    flash(f'Doctor {name} added. Default password: Doctor@123', 'success')
    return redirect(url_for('admin_dashboard'))

# ── Seed ─────────────────────────────────────────────────────────────────────

def seed_data():
    if User.query.count() == 0:
        admin = User(name='Admin', email='admin@medai.com',
                     password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.flush()

        slots = json.dumps(['09:00', '10:00', '11:00', '14:00', '15:00'])
        doctors_data = [
            ('Dr. Priya Sharma', 'General Physician', 'priya@medai.com'),
            ('Dr. Rahul Mehta',  'Cardiologist',      'rahul@medai.com'),
            ('Dr. Sneha Patil',  'Dermatologist',     'sneha@medai.com'),
        ]
        for name, spec, email in doctors_data:
            u = User(name=name, email=email,
                     password=generate_password_hash('Doctor@123'), role='doctor')
            db.session.add(u)
            db.session.flush()
            db.session.add(Doctor(name=name, specialization=spec,
                                  available_slots=slots, user_id=u.id))
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, port=5000)
# Add enumerate to Jinja2 globals
import builtins
app.jinja_env.globals['enumerate'] = builtins.enumerate
