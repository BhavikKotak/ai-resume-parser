import os
import pandas as pd
from models import db, User, Candidate, UploadHistory
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from parser import extract_resume_text

from extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills,
    extract_education,
    extract_experience,
    extract_linkedin,
    extract_github,
    extract_certifications,
    extract_projects,
    extract_address
)

app = Flask(__name__)

app.config["SECRET_KEY"] = "smart_resume_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///smart_resume.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "resumes"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf", "docx"}

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_admin():
    return current_user.role == "admin"


def is_recruiter():
    return current_user.role == "recruiter"


def is_candidate():
    return current_user.role == "candidate"


@app.route("/")
def home():
    return redirect(url_for("login"))


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        existing = User.query.filter_by(email=email).first()

        if existing:
            flash("Email already exists")
            return redirect(url_for("register"))

        if User.query.count() == 0:
            role = "admin"

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role
        )

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return str(e)

        flash("Registration successful")
        return redirect(url_for("login"))

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))

            elif user.role == "recruiter":
                return redirect(url_for("recruiter_dashboard"))

            else:
                return redirect(url_for("candidate_dashboard"))

        flash("Invalid credentials")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("login"))


# ADMIN DASHBOARD
@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("candidate_dashboard"))

    candidates = Candidate.query.order_by(
        Candidate.upload_date.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        candidates=candidates,
        total_candidates=Candidate.query.count(),
        total_users=User.query.count(),
        total_uploads=UploadHistory.query.count()
    )

# RECRUITER DASHBOARD
@app.route("/recruiter/dashboard")
@login_required
def recruiter_dashboard():
    if current_user.role != "recruiter":
        flash("Access denied")
        return redirect(url_for("candidate_dashboard"))

    candidates = Candidate.query.order_by(
        Candidate.upload_date.desc()
    ).all()

    return render_template(
        "recruiter_dashboard.html",
        candidates=candidates,
        total_candidates=Candidate.query.count()
    )

# CANDIDATE DASHBOARD
@app.route("/candidate/dashboard")
@login_required
def candidate_dashboard():
    if not is_candidate():
        return redirect(url_for("login"))

    candidate = Candidate.query.filter_by(user_id=current_user.id).first()

    return render_template(
        "candidate_dashboard.html",
        candidate=candidate
    )
# UPLOAD
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_resume():
    if request.method == "POST":
        files = request.files.getlist("resume")

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                file.save(filepath)

                text = extract_resume_text(filepath)

                if is_candidate():
                    existing_candidate = Candidate.query.filter_by(
                        user_id=current_user.id
                    ).first()

                    if existing_candidate:
                        existing_candidate.name = extract_name(text)
                        existing_candidate.email = extract_email(text)
                        existing_candidate.phone = extract_phone(text)
                        existing_candidate.skills = ",".join(extract_skills(text))
                        existing_candidate.education = extract_education(text)
                        existing_candidate.experience = extract_experience(text)
                        existing_candidate.certifications = extract_certifications(text)
                        existing_candidate.linkedin = extract_linkedin(text)
                        existing_candidate.github = extract_github(text)
                        existing_candidate.address = extract_address(text)
                        existing_candidate.projects = extract_projects(text)
                        existing_candidate.resume_filename = filename

                    else:
                        candidate = Candidate(
                            user_id=current_user.id,
                            name=extract_name(text),
                            email=extract_email(text),
                            phone=extract_phone(text),
                            skills=",".join(extract_skills(text)),
                            education=extract_education(text),
                            experience=extract_experience(text),
                            certifications=extract_certifications(text),
                            linkedin=extract_linkedin(text),
                            github=extract_github(text),
                            address=extract_address(text),
                            projects=extract_projects(text),
                            resume_filename=filename,
                            status="New",
                            notes=""
                        )

                        db.session.add(candidate)

                else:
                    candidate = Candidate(
                        name=extract_name(text),
                        email=extract_email(text),
                        phone=extract_phone(text),
                        skills=",".join(extract_skills(text)),
                        education=extract_education(text),
                        experience=extract_experience(text),
                        certifications=extract_certifications(text),
                        linkedin=extract_linkedin(text),
                        github=extract_github(text),
                        address=extract_address(text),
                        projects=extract_projects(text),
                        resume_filename=filename,
                        status="New",
                        notes=""
                    )

                    db.session.add(candidate)

                history = UploadHistory(
                    filename=filename,
                    uploaded_by=current_user.username
                )

                db.session.add(history)

        db.session.commit()

        flash("Resume uploaded successfully")

        if is_admin():
            return redirect(url_for("admin_dashboard"))

        elif is_recruiter():
            return redirect(url_for("recruiter_dashboard"))

        else:
            return redirect(url_for("candidate_dashboard"))

    return render_template("upload.html")


# SEARCH
@app.route("/search")
@login_required
def search():
    if is_candidate():
        flash("Access denied")
        return redirect(url_for("candidate_dashboard"))

    query = request.args.get("query", "")

    candidates = Candidate.query.filter(
        (Candidate.name.like(f"%{query}%")) |
        (Candidate.skills.like(f"%{query}%")) |
        (Candidate.education.like(f"%{query}%"))
    ).all()

    if is_admin():
        return render_template(
            "admin_dashboard.html",
            candidates=candidates,
            total_candidates=Candidate.query.count(),
            total_users=User.query.count(),
            total_uploads=UploadHistory.query.count()
        )

    return render_template(
        "recruiter_dashboard.html",
        candidates=candidates,
        total_candidates=len(candidates)
    )

# CANDIDATE DETAIL
@app.route("/candidate/<int:id>")
@login_required
def candidate_detail(id):
    candidate = Candidate.query.get_or_404(id)

    if is_candidate():
        if candidate.user_id != current_user.id:
            flash("Access denied")
            return redirect(url_for("candidate_dashboard"))

    return render_template("candidate_detail.html", candidate=candidate)


# EDIT
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_candidate(id):
    candidate = Candidate.query.get_or_404(id)

    if is_candidate():
        if candidate.user_id != current_user.id:
            flash("Access denied")
            return redirect(url_for("candidate_dashboard"))

    if request.method == "POST":
        candidate.name = request.form["name"]
        candidate.email = request.form["email"]
        candidate.phone = request.form["phone"]
        candidate.skills = request.form["skills"]
        candidate.education = request.form["education"]
        candidate.experience = request.form["experience"]
        candidate.certifications = request.form["certifications"]
        candidate.linkedin = request.form["linkedin"]
        candidate.github = request.form["github"]
        candidate.address = request.form["address"]
        candidate.projects = request.form["projects"]
        candidate.status = request.form["status"]
        candidate.notes = request.form["notes"]

        db.session.commit()

        flash("Candidate updated")

        if is_candidate():
            return redirect(url_for("candidate_dashboard"))

        elif is_admin():
            return redirect(url_for("admin_dashboard"))

        else:
            return redirect(url_for("recruiter_dashboard"))

    return render_template("edit_candidate.html", candidate=candidate)

@app.route("/history")
@login_required
def history():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("candidate_dashboard"))

    uploads = UploadHistory.query.order_by(
        UploadHistory.upload_date.desc()
    ).all()

    return render_template("history.html", uploads=uploads)


@app.route("/export")
@login_required
def export_csv():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("candidate_dashboard"))

    candidates = Candidate.query.all()

    data = []

    for c in candidates:
        data.append({
            "Name": c.name,
            "Email": c.email,
            "Phone": c.phone,
            "Skills": c.skills,
            "Status": c.status
        })

    df = pd.DataFrame(data)
    df.to_csv("candidates.csv", index=False)

    return send_from_directory(".", "candidates.csv", as_attachment=True)


@app.route("/resume/<filename>")
@login_required
def view_resume(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )