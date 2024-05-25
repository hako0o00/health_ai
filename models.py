from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Doctor(db.Model):
    __tablename__ = 'doctors'
    idD = db.Column(db.Integer, primary_key=True)
    numtel =db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    speciality = db.Column(db.String(100), nullable=False)
    wilaya = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    avg_rating = db.Column(db.Float, nullable=True)

    visits = db.relationship('Visite', backref='doctor', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def calculate_avg_rating(self):
        if self.visits:
            self.avg_rating = sum(visit.rating for visit in self.visits) / len(self.visits)
        else:
            self.avg_rating = None

class Patient(db.Model):
    __tablename__ = 'patients'
    idP = db.Column(db.Integer, primary_key=True)
    numtel = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password_hash  = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    maladieCHRON = db.Column(db.String(128), nullable=True)
    traitement = db.Column(db.String(128), nullable=True)
    idD = db.Column(db.Integer, db.ForeignKey('idD'), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Visite(db.Model):
    __tablename__ = 'visits'
    idv = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    idD = db.Column(db.Integer, db.ForeignKey('idD'), nullable=False)
    idP = db.Column(db.Integer, db.ForeignKey('idP'), nullable=False)
    maladie=db.Column(db.String(100), nullable=True)
    diagnostic=db.Column(db.String(128), nullable=True)
    treatement=db.Column(db.String(128), nullable=True)

