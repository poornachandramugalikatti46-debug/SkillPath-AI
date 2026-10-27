import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv("data/student_training_data.csv")

print("Dataset loaded!")
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

# Numerical target
y = df["readiness_score"]


# ==========================================
# 3. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 4. Create Regression Model
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=10
)


# ==========================================
# 5. Train Model
# ==========================================

print("\nTraining Random Forest Regressor...")

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 6. Predictions
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 7. Evaluation
# ==========================================

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, y_pred)


print("\n==========================================")
print("REGRESSION RESULTS")
print("==========================================")

print(f"\nMAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# ==========================================
# 8. Show Actual vs Predicted
# ==========================================

results = pd.DataFrame({
    "Actual Score": y_test.values,
    "Predicted Score": np.round(y_pred, 2)
})

print("\nActual vs Predicted:")

print(results.head(10))


# ==========================================
# 9. Feature Importance
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
# 10. Save Model
# ==========================================

model_path = "models/readiness_regressor.joblib"

joblib.dump(model, model_path)

print("\nRegression model saved!")
print("Location:", model_path)