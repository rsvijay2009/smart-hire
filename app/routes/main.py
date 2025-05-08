from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from ..services.file_service import extract_text_from_file
from ..services.nlp_service import extract_skills_experience, calculate_match_score
from ..services.db_service import store_candidate, get_candidates_by_job_id
import uuid
import os
import logging

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    job_path = os.path.join(current_app.config["UPLOAD_FOLDER"])
    upload_folder = os.path.join(os.getcwd(), "uploads")
    job_description_path = os.path.join(upload_folder, "job_description.txt")
    return render_template("index.html", upload_folder=upload_folder, job_description_path=job_description_path)

@main_bp.route("/upload", methods=["POST"])
def upload_files():
    """Handle file uploads and process candidate matching."""
    if "job_description" not in request.files or "resumes" not in request.files:
        flash("Please upload both job description and resumes.")
        return redirect(url_for("main.index"))

    job_file = request.files["job_description"]
    resume_files = request.files.getlist("resumes")

    if job_file.filename == "" or not resume_files:
        flash("No files selected.")
        return redirect(url_for("main.index"))

    # Validate job file
    if not allowed_file(job_file.filename):
        flash("Invalid job description file type. Use PDF or TXT.")
        return redirect(url_for("main.index"))

    # Generate job ID
    job_id = str(uuid.uuid4())

    # Process job description
    job_filename = secure_filename(job_file.filename)
    job_path = os.path.join(current_app.config["UPLOAD_FOLDER"], job_filename)
    job_file.save(job_path)
    job_text = extract_text_from_file(job_path)

    if not job_text.strip():
        flash("Could not extract text from job description.")
        return redirect(url_for("main.index"))

    # Extract job requirements
    job_skills, job_experience = extract_skills_experience(job_text)
    if not job_skills:
        flash("No skills identified in job description. Please include specific skills.")
        return redirect(url_for("main.index"))

    # Process resumes
    candidates = []
    for resume in resume_files:
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            resume_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            resume.save(resume_path)
            resume_text = extract_text_from_file(resume_path)

            if not resume_text.strip():
                flash(f"Could not extract text from {filename}. Skipping.")
                continue

            match_score, skills, experience, qualifications = calculate_match_score(
                job_text, resume_text, job_skills, job_experience
            )

            # Store candidate
            store_candidate(
                filename, resume_text, skills, experience, qualifications, match_score, job_id
            )

            candidates.append({
                "name": filename,
                "skills": skills,
                "experience": experience,
                "qualifications": qualifications,
                "match_score": round(match_score * 100, 2)
            })

    if not candidates:
        flash("No valid resumes processed.")
        return redirect(url_for("main.index"))

    # Sort candidates by match score
    candidates = sorted(candidates, key=lambda x: x["match_score"], reverse=True)

    return render_template("results.html", candidates=candidates, job_id=job_id)

@main_bp.route("/history/<job_id>")
def view_history(job_id):
    """View historical candidate data for a job."""
    candidates = get_candidates_by_job_id(job_id)
    return render_template("results.html", candidates=candidates, job_id=job_id)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]
    )
