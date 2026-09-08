"""
Tech Stack Recommender
-----------------------
Project 3 Capstone (DecodeLabs) — AI Recommendation Logic

Maps a user's raw skills/interests to the most relevant tech job roles
using Content-Based Filtering: TF-IDF feature weighting + Cosine Similarity.

Pipeline (per the brief):
  1. Ingestion  -> capture user state (min. 3 skill inputs)
  2. Scoring    -> TF-IDF vectorize + Cosine Similarity vs each job role
  3. Sorting    -> rank scores descending
  4. Filtering  -> truncate to Top-N recommendations

No external ML libraries required — TF-IDF and cosine similarity are
implemented from scratch so the underlying math is visible.
"""

import csv
import math
import os
from collections import Counter


# --------------------------------------------------------------------------- #
# 1. DATA LOADING
# --------------------------------------------------------------------------- #

def load_job_roles_from_csv(path):
    """
    Expects a CSV with columns: role_name, skills
    where 'skills' is a semicolon-separated list of tags, e.g.:

        role_name,skills
        Data Scientist,Python;SQL;Machine Learning;Data Analysis;Statistics
        DevOps Engineer,AWS;Docker;Kubernetes;CI/CD;Automation

    Returns: dict[str, list[str]]  ->  {role_name: [skill_tags...]}
    """
    roles = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            role = row["role_name"].strip()
            skills = [s.strip() for s in row["skills"].split(";") if s.strip()]
            roles[role] = skills
    return roles


def sample_job_roles():
    """
    Fallback dataset (used when raw_skills.csv isn't provided) so the
    script runs standalone. Swap this out for load_job_roles_from_csv(path)
    once you have your real raw_skills.csv.
    """
    return {
        "Data Scientist": [
            "Python", "SQL", "Machine Learning", "Statistics",
            "Data Analysis", "Pandas", "Data Visualization",
        ],
        "DevOps Engineer": [
            "AWS", "Docker", "Kubernetes", "CI/CD",
            "Automation", "Linux", "Cloud Computing",
        ],
        "Backend Developer": [
            "Java", "Python", "SQL", "APIs",
            "Data Structures", "System Design", "Git",
        ],
        "Cloud Architect": [
            "AWS", "Cloud Computing", "Automation",
            "Kubernetes", "System Design", "Networking",
        ],
        "Frontend Developer": [
            "JavaScript", "React", "HTML", "CSS",
            "UI Design", "Git", "Web Design",
        ],
        "Machine Learning Engineer": [
            "Python", "Machine Learning", "TensorFlow",
            "Neural Networks", "Data Structures", "Statistics",
        ],
        "Systems Administrator": [
            "Linux", "Networking", "Automation",
            "Cloud Computing", "Docker", "Security",
        ],
        "Full Stack Developer": [
            "JavaScript", "React", "Python", "SQL",
            "APIs", "Git", "System Design",
        ],
    }


# --------------------------------------------------------------------------- #
# 2. VECTORIZATION: TF-IDF
# --------------------------------------------------------------------------- #

def build_vocabulary(documents):
    """documents: list[list[str]] of tag lists -> sorted unique vocabulary list."""
    vocab = set()
    for doc in documents:
        vocab.update(doc)
    return sorted(vocab)


def compute_tf(doc_tags, vocabulary):
    """
    Term Frequency for one document (role's skill list).
    TF = (count of term in doc) / (total terms in doc)
    """
    total_terms = len(doc_tags) or 1
    counts = Counter(doc_tags)
    return [counts.get(term, 0) / total_terms for term in vocabulary]


def compute_idf(documents, vocabulary):
    """
    Inverse Document Frequency across all documents.
    IDF = log(total_documents / documents_containing_term)
    """
    n_docs = len(documents)
    idf = []
    for term in vocabulary:
        doc_count = sum(1 for doc in documents if term in doc)
        idf.append(math.log(n_docs / doc_count) if doc_count else 0.0)
    return idf


def tfidf_vector(doc_tags, vocabulary, idf):
    tf = compute_tf(doc_tags, vocabulary)
    return [tf_val * idf_val for tf_val, idf_val in zip(tf, idf)]


# --------------------------------------------------------------------------- #
# 3. SCORING: COSINE SIMILARITY
# --------------------------------------------------------------------------- #

def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))


def magnitude(v):
    return math.sqrt(sum(x * x for x in v))


def cosine_similarity(vec_a, vec_b):
    mag_a, mag_b = magnitude(vec_a), magnitude(vec_b)
    if mag_a == 0 or mag_b == 0:
        return 0.0  # cold-start guard: no overlap possible
    return dot_product(vec_a, vec_b) / (mag_a * mag_b)


# --------------------------------------------------------------------------- #
# 4. RECOMMENDATION PIPELINE (Ingestion -> Scoring -> Sorting -> Filtering)
# --------------------------------------------------------------------------- #

def recommend_tech_stack(user_skills, job_roles, top_n=3):
    """
    user_skills : list[str]  (minimum 3 skill tags, per project spec)
    job_roles   : dict[str, list[str]]  {role_name: [skill_tags...]}
    top_n       : int, number of top matches to return

    Returns: list[tuple[str, float]] sorted by descending similarity score.
    """
    if len(user_skills) < 3:
        raise ValueError("Please provide at least 3 skills for accurate matching.")

    role_names = list(job_roles.keys())
    role_docs = list(job_roles.values())

    # Shared vocabulary must include the user's tags too, so unseen
    # user skills don't just vanish from the vector space.
    all_documents = role_docs + [user_skills]
    vocabulary = build_vocabulary(all_documents)
    idf = compute_idf(all_documents, vocabulary)

    # Vectorize every job role
    role_vectors = {
        name: tfidf_vector(tags, vocabulary, idf)
        for name, tags in job_roles.items()
    }

    # Vectorize the user profile the same way
    user_vector = tfidf_vector(user_skills, vocabulary, idf)

    # --- Scoring ---
    scores = [
        (name, cosine_similarity(user_vector, role_vectors[name]))
        for name in role_names
    ]

    # --- Sorting ---
    scores.sort(key=lambda pair: pair[1], reverse=True)

    # --- Filtering (Top-N) ---
    return scores[:top_n]


# --------------------------------------------------------------------------- #
# 5. DEMO / CLI ENTRY POINT
# --------------------------------------------------------------------------- #

def main():
    csv_path = "raw_skills.csv"
    if os.path.exists(csv_path):
        job_roles = load_job_roles_from_csv(csv_path)
        print(f"Loaded {len(job_roles)} job roles from {csv_path}\n")
    else:
        job_roles = sample_job_roles()
        print("raw_skills.csv not found — using built-in sample dataset.\n")

    print("Available job roles:", ", ".join(job_roles.keys()))
    print()

    # Example input (matches the slide's worked example)
    user_skills = ["Python", "Cloud Computing", "Automation"]
    print(f"User input skills: {user_skills}\n")

    results = recommend_tech_stack(user_skills, job_roles, top_n=3)

    print("Top recommended career paths:")
    for rank, (role, score) in enumerate(results, start=1):
        print(f"  {rank}. {role:<28} similarity = {score:.4f} ({score*100:.1f}% match)")


if __name__ == "__main__":
    main()