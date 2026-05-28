from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="candidate")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

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

    status = db.Column(db.String(50), default="New")

    notes = db.Column(db.Text)

    resume_filename = db.Column(db.String(300))

    upload_date = db.Column(db.DateTime, default=datetime.utcnow)


class UploadHistory(db.Model):
    __tablename__ = "upload_history"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(300))

    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    uploaded_by = db.Column(db.String(150))