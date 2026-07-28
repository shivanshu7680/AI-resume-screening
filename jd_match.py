from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_jd_match(resume_text, job_description):

    if not job_description.strip():
        return None

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    score = cosine_similarity(vectors)[0][1]

    return round(score * 100, 2)