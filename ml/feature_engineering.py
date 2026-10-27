import pandas as pd

# --------------------------------------------------
# Features expected by our ML models
# --------------------------------------------------

MODEL_FEATURES = [
    "cgpa",

    "python_score",
    "java_score",
    "sql_score",
    "dsa_score",
    "frontend_score",
    "backend_score",
    "ml_score",
    "cloud_score",

    "resume_skill_count",
    "project_count",
    "internship_count",
    "certification_count",
    "experience_months",

    "github_repo_count",
    "github_language_count",
    "github_star_count",
    "github_fork_count",
    "github_project_count",
    "github_activity_score",

    "technical_score",
    "aptitude_score",
    "problem_solving_score",
    "communication_score",
    "interview_confidence_score"
]

# --------------------------------------------------
# Create empty student
# --------------------------------------------------

def create_empty_student():
    return {
        feature: 0
        for feature in MODEL_FEATURES
    }

# --------------------------------------------------
# Safe number conversion
# --------------------------------------------------

def safe_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

# --------------------------------------------------
# Resume -> General Features
# --------------------------------------------------

def add_resume_features(features, resume_data):
    if not resume_data:
        return features

    features["resume_skill_count"] = safe_float(
        resume_data.get("skill_count", 0)
    )
    features["project_count"] = safe_float(
        resume_data.get("project_count", 0)
    )
    features["internship_count"] = safe_float(
        resume_data.get("internship_count", 0)
    )
    features["certification_count"] = safe_float(
        resume_data.get("certification_count", 0)
    )
    features["experience_months"] = safe_float(
        resume_data.get("experience_months", 0)
    )

    return features

# --------------------------------------------------
# Resume Skills -> Numerical Features
# --------------------------------------------------

def add_skill_features(student, skills, skill_profile=None):
    skills_lower = {
        str(skill).lower().strip()
        for skill in skills
    }
    skill_profile = skill_profile or {}

    def get_skill_score(skill_name, default=20):
        score = skill_profile.get(skill_name, default)
        return max(0, min(100, safe_float(score)))

    if "python" in skills_lower:
        student["python_score"] = get_skill_score("python")

    if "java" in skills_lower:
        student["java_score"] = get_skill_score("java")

    if (
        "sql" in skills_lower
        or "mysql" in skills_lower
        or "postgresql" in skills_lower
        or "postgres" in skills_lower
    ):
        student["sql_score"] = get_skill_score("sql")

    if (
        "data structures" in skills_lower
        or "algorithms" in skills_lower
        or "dsa" in skills_lower
        or "problem solving" in skills_lower
    ):
        student["dsa_score"] = get_skill_score("problem solving")

    frontend_skills = {"react", "react.js", "html", "css"}
    if skills_lower.intersection(frontend_skills):
        frontend_scores = []
        if "react" in skills_lower or "react.js" in skills_lower:
            frontend_scores.append(get_skill_score("react"))
        if "html" in skills_lower:
            frontend_scores.append(get_skill_score("html", 20))
        if "css" in skills_lower:
            frontend_scores.append(get_skill_score("css", 20))
        if frontend_scores:
            student["frontend_score"] = max(frontend_scores)

    backend_scores = []
    if (
        "node.js" in skills_lower
        or "nodejs" in skills_lower
        or "node js" in skills_lower
    ):
        backend_scores.append(get_skill_score("node.js"))
    if "express.js" in skills_lower or "express" in skills_lower:
        backend_scores.append(get_skill_score("express.js"))
    if "mongodb" in skills_lower:
        backend_scores.append(get_skill_score("mongodb"))
    if (
        "rest api" in skills_lower
        or "rest apis" in skills_lower
        or "restful api" in skills_lower
        or "restful apis" in skills_lower
    ):
        backend_scores.append(get_skill_score("rest api"))
    if backend_scores:
        student["backend_score"] = max(backend_scores)

    if "machine learning" in skills_lower or "ml" in skills_lower:
        student["ml_score"] = get_skill_score("machine learning")

    cloud_skills = {"aws", "azure", "gcp", "cloud", "cloud computing"}
    if skills_lower.intersection(cloud_skills):
        student["cloud_score"] = 60

    return student

# --------------------------------------------------
# GitHub -> Features
# --------------------------------------------------

def add_github_features(student, github_data):
    if not github_data:
        return student

    student["github_repo_count"] = safe_float(
        github_data.get("github_repo_count", 0)
    )
    student["github_language_count"] = safe_float(
        github_data.get("github_language_count", 0)
    )
    student["github_star_count"] = safe_float(
        github_data.get("github_star_count", 0)
    )
    student["github_fork_count"] = safe_float(
        github_data.get("github_fork_count", 0)
    )
    student["github_project_count"] = safe_float(
        github_data.get("github_project_count", 0)
    )
    student["github_activity_score"] = safe_float(
        github_data.get("github_activity_score", 0)
    )

    return student

# --------------------------------------------------
# Assessment -> Features
# --------------------------------------------------

def add_assessment_features(student, assessment_data):
    if not assessment_data:
        return student

    student["technical_score"] = safe_float(
        assessment_data.get("technical_score", 0)
    )
    student["aptitude_score"] = safe_float(
        assessment_data.get("aptitude_score", 0)
    )
    student["problem_solving_score"] = safe_float(
        assessment_data.get("problem_solving_score", 0)
    )
    student["communication_score"] = safe_float(
        assessment_data.get("communication_score", 0)
    )
    student["interview_confidence_score"] = safe_float(
        assessment_data.get("interview_confidence_score", 0)
    )

    return student

# --------------------------------------------------
# Build final ML feature vector
# --------------------------------------------------

def build_feature_vector(
    profile,
    resume_data=None,
    github_data=None,
    assessment_data=None,
    skill_profile=None
):
    student = create_empty_student()

    if profile:
        student["cgpa"] = safe_float(profile.get("cgpa", 0))

    if resume_data:
        student = add_resume_features(student, resume_data)
        student = add_skill_features(
            student,
            resume_data.get("skills", []),
            skill_profile
        )

    student = add_github_features(student, github_data)
    student = add_assessment_features(student, assessment_data)

    feature_vector = pd.DataFrame([student])
    feature_vector = feature_vector[MODEL_FEATURES]

    return feature_vector

# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":
    profile = {"cgpa": 7.7}

    resume_data = {
        "skills": [
            "Python", "Java", "MySQL", "Git", "GitHub", "React",
            "Node.js", "Express.js", "MongoDB", "REST API",
            "Machine Learning", "Data Structures"
        ],
        "skill_count": 12,
        "project_count": 3,
        "internship_count": 0,
        "certification_count": 3,
        "experience_months": 0
    }

    skill_profile = {
        "python": 65,
        "java": 30,
        "sql": 20,
        "problem solving": 20,
        "react": 55,
        "node.js": 45,
        "express.js": 55,
        "mongodb": 45,
        "rest api": 45,
        "machine learning": 65
    }

    github_data = {
        "github_repo_count": 7,
        "github_language_count": 5,
        "github_star_count": 4,
        "github_fork_count": 0,
        "github_project_count": 7,
        "github_activity_score": 89
    }

    assessment_data = {
        "technical_score": 85,
        "aptitude_score": 75,
        "problem_solving_score": 65,
        "communication_score": 55,
        "interview_confidence_score": 75
    }

    features = build_feature_vector(
        profile=profile,
        resume_data=resume_data,
        github_data=github_data,
        assessment_data=assessment_data,
        skill_profile=skill_profile
    )

    print("\n===================================")
    print("    UNIFIED FEATURE ENGINEERING")
    print("===================================")
    print("\nGenerated Features:\n")
    print(features.to_string(index=False))
    print("\nNumber of features:", len(features.columns))
    print("\nFeature engineering successful!")