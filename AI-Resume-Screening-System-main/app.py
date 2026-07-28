from flask import Flask, render_template, request
import fitz
import joblib
import traceback
import os

from preprocess import clean_resume
from skills import extract_skills, get_missing_skills
from ats import calculate_ats_score
from jd_match import calculate_jd_match

# ==========================================================
# Flask Application
# ==========================================================

app = Flask(__name__)

# ==========================================================
# Configuration
# ==========================================================

UPLOAD_EXTENSIONS = {".pdf"}

MAX_CONTENT_LENGTH = 5 * 1024 * 1024

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# ==========================================================
# Professional Role Mapping
# ==========================================================

ROLE_MAPPING = {

    "Data Science": "Data Scientist",

    "HR": "Human Resources Executive",

    "Advocate": "Legal Associate",

    "Arts": "Graphic Designer",

    "Automation Testing": "Automation Test Engineer",

    "Blockchain": "Blockchain Developer",

    "Business Analyst": "Business Analyst",

    "Civil Engineer": "Civil Engineer",

    "Database": "Database Administrator",

    "DevOps Engineer": "DevOps Engineer",

    "DotNet Developer": ".NET Developer",

    "Electrical Engineering": "Electrical Engineer",

    "ETL Developer": "ETL Developer",

    "Hadoop": "Big Data Engineer",

    "Health and fitness": "Healthcare Consultant",

    "Java Developer": "Java Developer",

    "Mechanical Engineer": "Mechanical Engineer",

    "Network Security Engineer": "Cyber Security Analyst",

    "Operations Manager": "Operations Manager",

    "PMO": "Project Management Officer",

    "Python Developer": "Python Developer",

    "SAP Developer": "SAP Consultant",

    "Sales": "Sales Executive",

    "Testing": "QA Engineer",

    "Web Designing": "Frontend Web Developer"

}

# ==========================================================
# Load Machine Learning Models
# ==========================================================

try:

    print("=" * 60)

    print("Loading AI Models...")

    model = joblib.load("model/model.pkl")

    tfidf = joblib.load("model/tfidf.pkl")

    encoder = joblib.load("model/label_encoder.pkl")

    print("✓ model.pkl loaded")

    print("✓ tfidf.pkl loaded")

    print("✓ label_encoder.pkl loaded")

    print("=" * 60)

except Exception as e:

    print("\nModel Loading Failed\n")

    traceback.print_exc()

    raise e


# ==========================================================
# Helper Functions
# ==========================================================

def allowed_file(filename):

    extension = os.path.splitext(filename)[1].lower()

    return extension in UPLOAD_EXTENSIONS


def extract_text(pdf_file):

    text = ""

    pdf = fitz.open(

        stream=pdf_file.read(),

        filetype="pdf"

    )

    for page in pdf:

        text += page.get_text()

    pdf.close()

    return text


def predict_role(cleaned_resume):

    vector = tfidf.transform(

        [cleaned_resume]

    )

    prediction_encoded = model.predict(

        vector

    )[0]

    raw_role = encoder.inverse_transform(

        [prediction_encoded]

    )[0]

    confidence = round(

        max(

            model.predict_proba(vector)[0]

        ) * 100,

        2

    )

    professional_role = ROLE_MAPPING.get(raw_role)

    if professional_role is None:
        # Fallback: try a case/whitespace-insensitive match in case the
        # label encoder's exact string casing ever drifts from ROLE_MAPPING.
        normalized_target = raw_role.strip().lower()
        for key, value in ROLE_MAPPING.items():
            if key.strip().lower() == normalized_target:
                professional_role = value
                break

    if professional_role is None:
        professional_role = raw_role

    return professional_role, raw_role, confidence
# ==========================================================
# Resume Analysis Engine
# ==========================================================

def analyze_resume(resume_text, job_description=""):

    result = {

        "prediction": None,

        "raw_prediction": None,

        "confidence": None,

        "skills": [],

        "missing_skills": [],

        "ats_score": None,

        "jd_match": None

    }

    # --------------------------------------------
    # Clean Resume
    # --------------------------------------------

    cleaned_resume = clean_resume(

        resume_text

    )

    # --------------------------------------------
    # Extract Skills
    # --------------------------------------------

    skills = extract_skills(

        resume_text

    )

    result["skills"] = skills

    # --------------------------------------------
    # ATS Score
    # --------------------------------------------

    result["ats_score"] = calculate_ats_score(

        resume_text,

        skills

    )

    # --------------------------------------------
    # Predict Job Role
    # --------------------------------------------

    prediction, raw_prediction, confidence = predict_role(

        cleaned_resume

    )

    result["prediction"] = prediction

    result["raw_prediction"] = raw_prediction

    result["confidence"] = confidence

    # --------------------------------------------
    # Missing Skills
    # --------------------------------------------

    result["missing_skills"] = get_missing_skills(

        raw_prediction,

        skills

    )

    # --------------------------------------------
    # JD Match
    # --------------------------------------------

    if job_description.strip():

        result["jd_match"] = calculate_jd_match(

            resume_text,

            job_description

        )

    else:

        result["jd_match"] = None

    return result


# ==========================================================
# Console Logger
# ==========================================================

def print_report(report):

    print("\n")

    print("=" * 70)

    print("AI RESUME ANALYSIS REPORT")

    print("=" * 70)

    print(

        "Professional Role :",

        report["prediction"]

    )

    print(

        "Dataset Category  :",

        report["raw_prediction"]

    )

    print(

        "Confidence        :",

        str(report["confidence"]) + "%"

    )

    print(

        "ATS Score         :",

        report["ats_score"]

    )

    print(

        "JD Match          :",

        report["jd_match"]

    )

    print(

        "Detected Skills"

    )

    for skill in report["skills"]:

        print("   ✓", skill)

    print()

    print(

        "Missing Skills"

    )

    if len(report["missing_skills"]) == 0:

        print("   None")

    else:

        for skill in report["missing_skills"]:

            print("   ✗", skill)

    print("=" * 70)

    print()


# ==========================================================
# Upload Validator
# ==========================================================

def validate_upload(file):

    if file is None:

        return False, "Please upload a resume."

    if file.filename == "":

        return False, "Please choose a PDF file."

    if not allowed_file(file.filename):

        return False, "Only PDF files are allowed."

    return True, None
# ==========================================================
# Home Route
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    data = {

        "prediction": None,

        "confidence": None,

        "filename": None,

        "error": None,

        "skills": [],

        "missing_skills": [],

        "ats_score": None,

        "jd_match": None

    }

    if request.method == "POST":

        print("\n")

        print("=" * 70)

        print("Resume Uploaded")

        print("=" * 70)

        try:

            file = request.files.get(

                "resume"

            )

            valid, error = validate_upload(

                file

            )

            if not valid:

                data["error"] = error

                return render_template(

                    "index.html",

                    **data

                )

            data["filename"] = file.filename

            print(

                "Reading PDF..."

            )

            resume_text = extract_text(

                file

            )

            print(

                "Resume Length :",

                len(resume_text)

            )

            job_description = request.form.get(

                "job_description",

                ""

            )

            report = analyze_resume(

                resume_text,

                job_description

            )

            print_report(

                report

            )

            data.update(report)

        except Exception as e:

            traceback.print_exc()

            data["error"] = str(e)

            print(

                "\nError :",

                e

            )

    return render_template(

        "index.html",

        prediction=data["prediction"],

        confidence=data["confidence"],

        filename=data["filename"],

        skills=data["skills"],

        missing_skills=data["missing_skills"],

        ats_score=data["ats_score"],

        jd_match=data["jd_match"],

        error=data["error"]

    )


# ==========================================================
# Error Pages
# ==========================================================

@app.errorhandler(404)

def page_not_found(error):

    return render_template(

        "index.html",

        error="Page Not Found"

    ), 404


@app.errorhandler(413)

def file_too_large(error):

    return render_template(

        "index.html",

        error="Maximum PDF size is 5 MB."

    ), 413


@app.errorhandler(500)

def internal_server_error(error):

    return render_template(

        "index.html",

        error="Internal Server Error"

    ), 500


# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    print()

    print("=" * 70)

    print("AI Resume Screening System Started")

    print("URL : http://127.0.0.1:5000")

    print("=" * 70)

    print()

    app.run(

        debug=True

    )