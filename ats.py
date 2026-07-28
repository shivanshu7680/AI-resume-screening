"""
===========================================================
                AI RESUME ATS ENGINE v2.0
===========================================================

Author : Sharad Verma
Purpose :
Professional ATS Resume Score Calculator

Features
--------
✓ Contact Information Detection
✓ Resume Section Detection
✓ Education Analysis
✓ Experience Analysis
✓ Projects Analysis
✓ Technical Skills Analysis
✓ Certifications
✓ ATS Formatting
✓ Resume Length
✓ Action Verbs
✓ Quantified Achievements
✓ Keyword Matching
✓ AI Suggestions

===========================================================
"""

import re
import math
from collections import Counter


# ==========================================================
# ATS CONFIGURATION
# ==========================================================

MAX_SCORE = 100

IDEAL_MIN_WORDS = 450
IDEAL_MAX_WORDS = 900

MIN_PROJECTS = 3

MIN_SKILLS = 10

MIN_CERTIFICATIONS = 2


# ==========================================================
# CONTACT REGEX
# ==========================================================

EMAIL_REGEX = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

PHONE_REGEX = re.compile(
    r"(\+91[\-\s]?)?[6-9]\d{9}"
)

LINKEDIN_REGEX = re.compile(
    r"(linkedin\.com\/in\/[A-Za-z0-9_-]+)"
)

GITHUB_REGEX = re.compile(
    r"(github\.com\/[A-Za-z0-9_-]+)"
)

URL_REGEX = re.compile(
    r"https?:\/\/[^\s]+"
)


# ==========================================================
# ACTION VERBS
# ==========================================================

ACTION_VERBS = {

    "developed",
    "created",
    "built",
    "implemented",
    "optimized",
    "engineered",
    "managed",
    "led",
    "improved",
    "designed",
    "integrated",
    "automated",
    "analyzed",
    "achieved",
    "reduced",
    "increased",
    "trained",
    "deployed",
    "generated",
    "solved",
    "maintained",
    "configured",
    "delivered",
    "collaborated",
    "supported",
    "initiated",
    "planned",
    "organized",
    "executed",
    "tested"

}


# ==========================================================
# STANDARD RESUME SECTIONS
# ==========================================================

SECTION_KEYWORDS = {

    "summary": [

        "summary",
        "professional summary",
        "profile",
        "objective"

    ],

    "education": [

        "education",
        "academic"

    ],

    "experience": [

        "experience",
        "employment",
        "work experience"

    ],

    "projects": [

        "projects",
        "project"

    ],

    "skills": [

        "skills",
        "technical skills"

    ],

    "certifications": [

        "certification",
        "certifications"

    ],

    "achievements": [

        "achievement",
        "achievements"

    ]

}


# ==========================================================
# EDUCATION KEYWORDS
# ==========================================================

EDUCATION_KEYWORDS = [

    "b.tech",
    "b.e",
    "bachelor",
    "m.tech",
    "m.e",
    "mca",
    "bca",
    "b.sc",
    "m.sc",
    "phd",
    "degree",
    "cgpa",
    "gpa"

]


# ==========================================================
# EXPERIENCE KEYWORDS
# ==========================================================

EXPERIENCE_KEYWORDS = [

    "experience",
    "intern",
    "internship",
    "developer",
    "engineer",
    "analyst",
    "consultant",
    "associate",
    "software engineer",
    "data scientist"

]


# ==========================================================
# PROJECT KEYWORDS
# ==========================================================

PROJECT_KEYWORDS = [

    "project",
    "developed",
    "built",
    "implemented",
    "github",
    "streamlit",
    "flask",
    "react",
    "django"

]


# ==========================================================
# CERTIFICATION PROVIDERS
# ==========================================================

CERTIFICATION_KEYWORDS = [

    "oracle",
    "aws",
    "google",
    "microsoft",
    "ibm",
    "coursera",
    "udemy",
    "nptel",
    "tcs",
    "infosys",
    "deloitte",
    "cisco",
    "meta",
    "edx"

]


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def clean_text(text):

    if text is None:
        return ""

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


def word_count(text):

    return len(text.split())


def count_occurrences(text, keywords):

    count = 0

    for keyword in keywords:

        count += text.count(keyword.lower())

    return count


def contains_any(text, keywords):

    for keyword in keywords:

        if keyword.lower() in text:

            return True

    return False


# ==========================================================
# CONTACT ANALYZER
# ==========================================================

def analyze_contact_information(text):

    score = 0

    report = {}

    report["email"] = bool(
        EMAIL_REGEX.search(text)
    )

    report["phone"] = bool(
        PHONE_REGEX.search(text)
    )

    report["linkedin"] = bool(
        LINKEDIN_REGEX.search(text)
    )

    report["github"] = bool(
        GITHUB_REGEX.search(text)
    )

    report["portfolio"] = len(
        URL_REGEX.findall(text)
    ) > 0

    if report["email"]:
        score += 2

    if report["phone"]:
        score += 2

    if report["linkedin"]:
        score += 2

    if report["github"]:
        score += 2

    if report["portfolio"]:
        score += 2

    report["score"] = score

    return report
# ==========================================================
# RESUME SECTION DETECTION ENGINE
# ==========================================================

SECTION_WEIGHTS = {

    "summary": 2,

    "education": 3,

    "experience": 4,

    "projects": 3,

    "skills": 2,

    "certifications": 1,

    "achievements": 1

}


def detect_resume_sections(text):

    """
    Detects standard resume sections.

    Returns

    {

        "sections": {},

        "score": int,

        "missing": []

    }

    """

    text = clean_text(text)

    result = {

        "sections": {},

        "score": 0,

        "missing": []

    }

    total_score = 0

    for section_name, keywords in SECTION_KEYWORDS.items():

        found = False

        found_keyword = ""

        for keyword in keywords:

            if keyword in text:

                found = True

                found_keyword = keyword

                break

        result["sections"][section_name] = {

            "found": found,

            "matched_keyword": found_keyword

        }

        if found:

            total_score += SECTION_WEIGHTS.get(section_name, 0)

        else:

            result["missing"].append(section_name)

    result["score"] = total_score

    return result


# ==========================================================
# SECTION ORDER CHECKER
# ==========================================================

IDEAL_SECTION_ORDER = [

    "summary",

    "education",

    "experience",

    "projects",

    "skills",

    "certifications",

    "achievements"

]


def analyze_section_order(text):

    """

    Detects if sections are arranged properly.

    """

    text = clean_text(text)

    positions = {}

    for section in IDEAL_SECTION_ORDER:

        pos = -1

        for keyword in SECTION_KEYWORDS[section]:

            idx = text.find(keyword)

            if idx != -1:

                pos = idx

                break

        positions[section] = pos

    score = 5

    previous = -1

    disorder = []

    for section in IDEAL_SECTION_ORDER:

        current = positions[section]

        if current == -1:

            continue

        if current < previous:

            disorder.append(section)

            score -= 1

        previous = current

    if score < 0:

        score = 0

    return {

        "score": score,

        "positions": positions,

        "incorrect_order": disorder

    }


# ==========================================================
# RESUME SUMMARY ANALYZER
# ==========================================================

SUMMARY_KEYWORDS = [

    "machine learning",

    "python",

    "software",

    "developer",

    "engineer",

    "artificial intelligence",

    "data",

    "analysis",

    "nlp",

    "cloud"

]


def analyze_summary(text):

    """

    Evaluates professional summary.

    """

    text = clean_text(text)

    score = 0

    report = {}

    summary_found = False

    summary_text = ""

    for keyword in SECTION_KEYWORDS["summary"]:

        if keyword in text:

            summary_found = True

            start = text.find(keyword)

            summary_text = text[start:start + 700]

            break

    report["found"] = summary_found

    if not summary_found:

        report["score"] = 0

        report["issues"] = [

            "Professional summary not found."

        ]

        return report

    issues = []

    words = len(summary_text.split())

    report["word_count"] = words

    if 40 <= words <= 120:

        score += 4

    elif 25 <= words < 40:

        score += 2

    else:

        issues.append(

            "Summary length should be between 40 and 120 words."

        )

    keyword_hits = count_occurrences(

        summary_text,

        SUMMARY_KEYWORDS

    )

    report["keyword_hits"] = keyword_hits

    if keyword_hits >= 5:

        score += 4

    elif keyword_hits >= 3:

        score += 3

    elif keyword_hits >= 1:

        score += 1

    else:

        issues.append(

            "Summary lacks technical keywords."

        )

    if any(

        verb in summary_text

        for verb in ACTION_VERBS

    ):

        score += 2

    else:

        issues.append(

            "Summary should include action-oriented language."

        )

    report["score"] = score

    report["issues"] = issues

    return report


# ==========================================================
# MASTER SECTION ANALYZER
# ==========================================================

def analyze_resume_structure(text):

    """

    Runs all structure-related analyzers.

    """

    return {

        "sections": detect_resume_sections(text),

        "section_order": analyze_section_order(text),

        "summary": analyze_summary(text)

    }
# ==========================================================
# EDUCATION ANALYSIS ENGINE
# ==========================================================

DEGREE_KEYWORDS = {

    "phd": 10,

    "doctorate": 10,

    "m.tech": 9,

    "m.e": 9,

    "master": 9,

    "mba": 8,

    "mca": 8,

    "b.tech": 8,

    "b.e": 8,

    "bachelor": 7,

    "bca": 7,

    "b.sc": 6,

    "bcom": 5,

    "ba": 5,

    "diploma": 4

}


TOP_UNIVERSITIES = [

    "iit",

    "iisc",

    "iiit",

    "nit",

    "bits",

    "vit",

    "srm",

    "amity",

    "kiit",

    "lpu",

    "babu banarasi das",

    "bbdu"

]


RELEVANT_COURSES = [

    "data structures",

    "algorithms",

    "operating systems",

    "computer networks",

    "dbms",

    "machine learning",

    "artificial intelligence",

    "deep learning",

    "compiler design",

    "cloud computing",

    "software engineering",

    "statistics",

    "probability"

]


CGPA_PATTERN = re.compile(

    r"(cgpa|gpa)\s*[:\-]?\s*(\d+(\.\d+)?)"

)


YEAR_PATTERN = re.compile(

    r"(20\d{2})"

)


# ==========================================================
# DEGREE DETECTOR
# ==========================================================

def detect_degree(text):

    text = clean_text(text)

    detected = None

    score = 0

    for degree, marks in DEGREE_KEYWORDS.items():

        if degree in text:

            detected = degree

            score = marks

            break

    return {

        "degree": detected,

        "score": score

    }


# ==========================================================
# CGPA ANALYZER
# ==========================================================

def analyze_cgpa(text):

    text = clean_text(text)

    match = CGPA_PATTERN.search(text)

    if not match:

        return {

            "cgpa": None,

            "score": 0

        }

    cgpa = float(match.group(2))

    if cgpa >= 9:

        marks = 10

    elif cgpa >= 8:

        marks = 8

    elif cgpa >= 7:

        marks = 6

    elif cgpa >= 6:

        marks = 4

    else:

        marks = 2

    return {

        "cgpa": cgpa,

        "score": marks

    }


# ==========================================================
# UNIVERSITY ANALYZER
# ==========================================================

def analyze_university(text):

    text = clean_text(text)

    found = None

    score = 0

    for university in TOP_UNIVERSITIES:

        if university in text:

            found = university

            score = 5

            break

    return {

        "university": found,

        "score": score

    }


# ==========================================================
# COURSEWORK ANALYZER
# ==========================================================

def analyze_coursework(text):

    text = clean_text(text)

    detected = []

    for course in RELEVANT_COURSES:

        if course in text:

            detected.append(course)

    count = len(detected)

    if count >= 8:

        score = 5

    elif count >= 5:

        score = 4

    elif count >= 3:

        score = 3

    elif count >= 1:

        score = 2

    else:

        score = 0

    return {

        "courses": detected,

        "count": count,

        "score": score

    }


# ==========================================================
# EDUCATION YEAR ANALYZER
# ==========================================================

def analyze_graduation_year(text):

    text = clean_text(text)

    years = YEAR_PATTERN.findall(text)

    years = sorted(list(set(years)))

    if len(years) >= 2:

        return {

            "education_duration": f"{years[0]}-{years[-1]}",

            "score": 2

        }

    return {

        "education_duration": None,

        "score": 0

    }


# ==========================================================
# COMPLETE EDUCATION ANALYSIS
# ==========================================================

def analyze_education(text):

    degree = detect_degree(text)

    cgpa = analyze_cgpa(text)

    university = analyze_university(text)

    coursework = analyze_coursework(text)

    duration = analyze_graduation_year(text)

    total = (

        degree["score"]

        + cgpa["score"]

        + university["score"]

        + coursework["score"]

        + duration["score"]

    )

    if total > 25:

        total = 25

    return {

        "degree": degree,

        "cgpa": cgpa,

        "university": university,

        "coursework": coursework,

        "duration": duration,

        "score": total

    }


# ==========================================================
# FINAL ATS SCORE (MASTER AGGREGATOR)
# ==========================================================
#
# This is the single entry point app.py calls. It combines every
# sub-analyzer already defined above (contact info, resume
# structure/sections/order/summary, and education) plus a bonus
# for detected technical skills, then normalizes everything onto
# a single 0-100 scale so the template's percentage bar and
# score-band checks (>=90 / >=75 / >=60) work correctly.
#
# NOTE: "experience", "projects", "certifications", and
# "quantified achievements" are listed in the module docstring
# as intended features but are not implemented as separate
# analyzers in this file, so they aren't part of the score below.
# If you want those to count, add analyzer functions for them
# (mirroring analyze_education) and fold their "score" into
# raw_total / max_possible the same way education is handled.
# ==========================================================

# Points available for the skills bonus. Full marks once a resume
# contains at least MIN_SKILLS matched skills (see extract_skills
# in skills.py, which is what produces the `skills` list passed in).
MAX_SKILLS_SCORE = 20

# Max points each component can contribute, used to normalize
# the final score to a 0-100 scale.
_CONTACT_MAX = 10             # analyze_contact_information
_STRUCTURE_MAX = 16 + 5 + 10  # sections(16) + section_order(5) + summary(10) = 31
_EDUCATION_MAX = 25           # analyze_education (already capped internally)
_MAX_POSSIBLE = _CONTACT_MAX + _STRUCTURE_MAX + _EDUCATION_MAX + MAX_SKILLS_SCORE


def calculate_ats_score(resume_text, skills=None):

    if skills is None:
        skills = []

    contact = analyze_contact_information(resume_text)
    structure = analyze_resume_structure(resume_text)
    education = analyze_education(resume_text)

    structure_score = (
        structure["sections"]["score"]
        + structure["section_order"]["score"]
        + structure["summary"]["score"]
    )

    skills_count = len(skills)
    skills_score = min(skills_count, MIN_SKILLS) / MIN_SKILLS * MAX_SKILLS_SCORE

    raw_total = (
        contact["score"]
        + structure_score
        + education["score"]
        + skills_score
    )

    final_score = (raw_total / _MAX_POSSIBLE) * MAX_SCORE

    # Clamp defensively in case future edits push raw_total out of range.
    final_score = max(0, min(final_score, MAX_SCORE))

    return round(final_score, 2)