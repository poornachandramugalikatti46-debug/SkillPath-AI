import numpy as np
import pandas as pd

# Reproducible results
np.random.seed(42)

NUMBER_OF_STUDENTS = 1000


# -----------------------------
# 1. Academic Features
# -----------------------------

cgpa = np.round(
    np.random.uniform(5.5, 10.0, NUMBER_OF_STUDENTS),
    2
)


# -----------------------------
# 2. Technical Skills
# -----------------------------

python_score = np.random.randint(30, 101, NUMBER_OF_STUDENTS)
java_score = np.random.randint(30, 101, NUMBER_OF_STUDENTS)
sql_score = np.random.randint(30, 101, NUMBER_OF_STUDENTS)
dsa_score = np.random.randint(25, 101, NUMBER_OF_STUDENTS)
frontend_score = np.random.randint(20, 101, NUMBER_OF_STUDENTS)
backend_score = np.random.randint(20, 101, NUMBER_OF_STUDENTS)
ml_score = np.random.randint(20, 101, NUMBER_OF_STUDENTS)
cloud_score = np.random.randint(20, 101, NUMBER_OF_STUDENTS)


# -----------------------------
# 3. Resume Features
# -----------------------------

resume_skill_count = np.random.randint(
    3, 26, NUMBER_OF_STUDENTS
)

project_count = np.random.randint(
    0, 9, NUMBER_OF_STUDENTS
)

internship_count = np.random.randint(
    0, 4, NUMBER_OF_STUDENTS
)

certification_count = np.random.randint(
    0, 8, NUMBER_OF_STUDENTS
)

experience_months = np.random.randint(
    0, 25, NUMBER_OF_STUDENTS
)


# -----------------------------
# 4. GitHub Features
# -----------------------------

github_repo_count = np.random.randint(
    0, 21, NUMBER_OF_STUDENTS
)

github_language_count = np.random.randint(
    0, 9, NUMBER_OF_STUDENTS
)

github_star_count = np.random.randint(
    0, 101, NUMBER_OF_STUDENTS
)

github_fork_count = np.random.randint(
    0, 31, NUMBER_OF_STUDENTS
)

github_project_count = np.random.randint(
    0, 11, NUMBER_OF_STUDENTS
)

github_activity_score = np.random.randint(
    0, 101, NUMBER_OF_STUDENTS
)


# -----------------------------
# 5. Assessment Features
# -----------------------------

technical_score = np.random.randint(
    25, 101, NUMBER_OF_STUDENTS
)

aptitude_score = np.random.randint(
    25, 101, NUMBER_OF_STUDENTS
)

problem_solving_score = np.random.randint(
    25, 101, NUMBER_OF_STUDENTS
)

communication_score = np.random.randint(
    25, 101, NUMBER_OF_STUDENTS
)

interview_confidence_score = np.random.randint(
    25, 101, NUMBER_OF_STUDENTS
)


# -----------------------------
# 6. Create DataFrame
# -----------------------------

df = pd.DataFrame({

    "cgpa": cgpa,

    "python_score": python_score,
    "java_score": java_score,
    "sql_score": sql_score,
    "dsa_score": dsa_score,
    "frontend_score": frontend_score,
    "backend_score": backend_score,
    "ml_score": ml_score,
    "cloud_score": cloud_score,

    "resume_skill_count": resume_skill_count,
    "project_count": project_count,
    "internship_count": internship_count,
    "certification_count": certification_count,
    "experience_months": experience_months,

    "github_repo_count": github_repo_count,
    "github_language_count": github_language_count,
    "github_star_count": github_star_count,
    "github_fork_count": github_fork_count,
    "github_project_count": github_project_count,
    "github_activity_score": github_activity_score,

    "technical_score": technical_score,
    "aptitude_score": aptitude_score,
    "problem_solving_score": problem_solving_score,
    "communication_score": communication_score,
    "interview_confidence_score": interview_confidence_score
})


# -----------------------------
# 7. Save Dataset
# -----------------------------

output_path = "data/student_training_data.csv"

df.to_csv(output_path, index=False)

print("Training dataset created successfully!")
print("Number of students:", len(df))
print("Number of features:", len(df.columns))
print("Saved to:", output_path)

print("\nFirst 5 rows:")
print(df.head())