from flask import Blueprint, request, jsonify
from models import db, Doctor, Patient, Visite

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/')
def index():
    return "The API is working"

@auth_blueprint.route('/doctor/signup', methods=['POST'])
def doctor_signup():
    data = request.get_json()
    doctor_id = data.get('idD')
    numtel = data.get('numtel')
    name = data['name']
    lastname = data['lastname']
    password = data['password_hash ']
    speciality = data['speciality']
    wilaya = data['wilaya']

    new_doctor = Doctor(doctor_id=idD, numtel=numtel, name=name, lastname=lastname, password=password_hash, speciality=speciality, wilaya=wilaya)
    new_doctor.password = password
    db.session.add(new_doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor registered successfully'}), 201

@auth_blueprint.route('/doctor/login', methods=['POST'])
def doctor_login():
    data = request.get_json()
    doctor_id = data['idD']
    password = data['password_hash ']

    doctor = Doctor.query.filter_by(id=id).first()
    if doctor and doctor.check_password(password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_blueprint.route('/patient/login', methods=['POST'])
def patient_login():
    data = request.get_json()
    patient_id = data['idP']
    password = data['password_hash']

    patient = Patient.query.filter_by(id=id).first()
    if patient and patient.check_password(password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_blueprint.route('/patient/signup', methods=['POST'])
def patient_signup():
    data = request.get_json()
    patient_id=data.get('idP')
    numtel = data.get('numtel')
    name = data['name']
    lastname = data['lastname']
    password = data['password_hash ']
    age = data.get('age')

    new_patient = Patient(patient_id=idP, numtel=numtel, name=name, lastname=lastname,password=password_hash, age=age)
    new_patient.password = password
    db.session.add(new_patient)
    db.session.commit()

    return jsonify({'message': 'Patient registered successfully'}), 201

@auth_blueprint.route('/visit', methods=['POST'])
def add_visit():
    data = request.get_json()
    rating = data['rating']
    doctor_id = data['doctor_id']
    patient_id = data['patient_id']

    new_visit = Visite(rating=rating, doctor_id=doctor_id, patient_id=patient_id)
    db.session.add(new_visit)

    doctor = Doctor.query.get(doctor_id)
    if doctor:
        doctor.calculate_avg_rating()

    db.session.commit()

    return jsonify({'message': 'Visit added and average rating updated successfully'}), 201
