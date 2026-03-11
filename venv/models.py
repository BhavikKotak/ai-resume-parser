from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200))

    email = db.Column(db.String(200))

    phone = db.Column(db.String(50))

    skills = db.Column(db.Text)

    education = db.Column(db.Text)

    experience = db.Column(db.Text)