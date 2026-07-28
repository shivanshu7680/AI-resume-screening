import re

# Master Skill List
SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Node.js",
    "Flask",
    "Django",
    "SQL",
    "MySQL",
    "MongoDB",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "Keras",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "NLP",
    "Power BI",
    "Excel",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Linux",
    "Tableau",
    "Spring Boot",
    "Hibernate",
    "Bootstrap"
]


# Required skills for each job category
SKILL_DATABASE = {

    "Data Science": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "Machine Learning",
        "Git",
        "Docker",
        "AWS",
        "Power BI"
    ],

    "Python Developer": [
        "Python",
        "Flask",
        "Django",
        "SQL",
        "Git",
        "Docker"
    ],

    "Java Developer": [
        "Java",
        "Spring Boot",
        "Hibernate",
        "SQL",
        "Git",
        "Docker"
    ],

    "Web Designing": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Bootstrap",
        "Git"
    ],

    "Testing": [
        "Java",
        "Selenium",
        "TestNG",
        "SQL",
        "Git"
    ],

    "DevOps Engineer": [
        "Docker",
        "AWS",
        "Linux",
        "Git",
        "Jenkins"
    ]
}


# Extract skills from resume
def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):
            found.append(skill)

    return sorted(list(set(found)))


# Find missing skills
def get_missing_skills(prediction, found_skills):

    required = SKILL_DATABASE.get(prediction, [])

    missing = []

    found_lower = [skill.lower() for skill in found_skills]

    for skill in required:

        if skill.lower() not in found_lower:
            missing.append(skill)

    return missing