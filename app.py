import os

from flask import Flask, render_template, request

from parser import extract_text_from_pdf

from extractor import (
extract_name,
extract_email,
extract_phone,
extract_skills,
extract_education,
extract_experience
)

from models import db, Candidate

app = Flask(__name__)

UPLOAD_FOLDER="resumes"

app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///resume.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db.init_app(app)


@app.route("/")
def home():

    return render_template("upload.html")


@app.route("/upload",methods=["POST"])
def upload_resume():

    file=request.files["resume"]

    filepath=os.path.join(app.config["UPLOAD_FOLDER"],file.filename)

    file.save(filepath)

    text=extract_text_from_pdf(filepath)

    name=extract_name(text)

    email=extract_email(text)

    phone=extract_phone(text)

    skills=extract_skills(text)

    education=extract_education(text)

    experience=extract_experience(text)

    candidate=Candidate(

        name=name,

        email=email,

        phone=phone,

        skills=",".join(skills),

        education=education,

        experience=experience

    )

    db.session.add(candidate)

    db.session.commit()

    return render_template("result.html",
                           name=name,
                           email=email,
                           phone=phone,
                           skills=skills,
                           education=education,
                           experience=experience)


@app.route("/dashboard")
def dashboard():

    candidates=Candidate.query.all()

    return render_template("dashboard.html",candidates=candidates)


@app.route("/search")
def search():

    skill=request.args.get("skill")

    candidates=Candidate.query.filter(Candidate.skills.like(f"%{skill}%")).all()

    return render_template("dashboard.html",candidates=candidates)


if __name__=="__main__":

    with app.app_context():

        db.create_all()

    app.run(debug=True)