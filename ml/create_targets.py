import pandas as pd
import numpy as np

# -----------------------------------
# 1. Load training data
# -----------------------------------

input_path = "data/student_training_data.csv"

df = pd.read_csv(input_path)


# -----------------------------------
# 2. Normalize project-related features
# -----------------------------------

project_score = np.minimum(df["project_count"] / 8 * 100, 100)

internship_score = np.minimum(
    df["internship_count"] / 3 * 100,
    100
)

experience_score = np.minimum(
    df["experience_months"] / 24 * 100,
    100
)

resume_score = np.minimum(
    df["resume_skill_count"] / 25 * 100,
    100
)


# -----------------------------------
# 3. Calculate technical skill score
# -----------------------------------

technical_skill_score = (
    df["python_score"] * 0.20 +
    df["java_score"] * 0.10 +
    df["sql_score"] * 0.15 +
    df["dsa_score"] * 0.15 +
    df["frontend_score"] * 0.10 +
    df["backend_score"] * 0.10 +
    df["ml_score"] * 0.10 +
    df["cloud_score"] * 0.10
)


# -----------------------------------
# 4. GitHub score
# -----------------------------------

github_score = (
    df["github_activity_score"] * 0.50
    + np.minimum(df["github_repo_count"] / 20 * 100, 100) * 0.20
    + np.minimum(df["github_project_count"] / 10 * 100, 100) * 0.20
    + np.minimum(df["github_language_count"] / 8 * 100, 100) * 0.10
)


# -----------------------------------
# 5. Assessment score
# -----------------------------------

assessment_score = (
    df["technical_score"] * 0.30
    + df["aptitude_score"] * 0.15
    + df["problem_solving_score"] * 0.25
    + df["communication_score"] * 0.15
    + df["interview_confidence_score"] * 0.15
)


# -----------------------------------
# 6. Education score
# -----------------------------------

education_score = (
    np.clip(
        (df["cgpa"] - 5.5) / 4.5 * 100,
        0,
        100
    )
)


# -----------------------------------
# 7. Final Career Readiness Index
# -----------------------------------

readiness_score = (
    technical_skill_score * 0.20
    + df["dsa_score"] * 0.15
    + assessment_score * 0.15
    + project_score * 0.15
    + internship_score * 0.10
    + resume_score * 0.10
    + github_score * 0.10
    + df["communication_score"] * 0.05
)

# Keep score between 0 and 100
readiness_score = np.clip(readiness_score, 0, 100)

# Round score
df["readiness_score"] = np.round(readiness_score, 2)


# -----------------------------------
# 8. Create readiness category
# -----------------------------------

def get_category(score):

    if score < 50:
        return "Low"

    elif score < 75:
        return "Medium"

    else:
        return "High"


df["readiness_category"] = df["readiness_score"].apply(
    get_category
)


# -----------------------------------
# 9. Save updated dataset
# -----------------------------------

output_path = "data/student_training_data.csv"

df.to_csv(output_path, index=False)


# -----------------------------------
# 10. Display results
# -----------------------------------

print("Targets created successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nSample results:")
print(
    df[
        [
            "readiness_score",
            "readiness_category"
        ]
    ].head(10)
)

print("\nCategory distribution:")
print(
    df["readiness_category"].value_counts()
)