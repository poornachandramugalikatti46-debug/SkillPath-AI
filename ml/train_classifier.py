import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import joblib


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv("data/student_training_data.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# 2. Select features
# ==========================================

features = [
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


X = df[features]

y = df["readiness_category"]


# ==========================================
# 3. Split dataset
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 4. Create model
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=10
)


# ==========================================
# 5. Train model
# ==========================================

print("\nTraining Random Forest...")

model.fit(X_train, y_train)

print("Model training completed!")


# ==========================================
# 6. Make predictions
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 7. Evaluate model
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\n==========================================")
print("MODEL RESULTS")
print("==========================================")

print("\nAccuracy:")
print(f"{accuracy:.4f}")


print("\nClassification Report:")
print(classification_report(y_test, y_pred))


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ==========================================
# 8. Feature Importance
# ==========================================

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nTop Important Features:")

print(importance.head(10))


# ==========================================
# 9. Save model
# ==========================================

model_path = "models/readiness_classifier.joblib"

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Location:", model_path)