from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    skills = db.Column(db.Text)
    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    certifications = db.Column(db.Text)
    linkedin = db.Column(db.String(300))
    github = db.Column(db.String(300))
    address = db.Column(db.Text)
    projects = db.Column(db.Text)
    resume_filename = db.Column(db.String(300))
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

class UploadHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    uploaded_by = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)