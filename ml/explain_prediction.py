import os
import sys
import joblib
import pandas as pd
import numpy as np
import shap


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ML_DIR = os.path.join(BASE_DIR, "ml")

sys.path.append(ML_DIR)


# ============================================================
# IMPORT FEATURE ENGINEERING
# ============================================================

from feature_engineering import build_feature_vector


# ============================================================
# MODEL PATH
# ============================================================

CLASSIFIER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "readiness_classifier.joblib"
)


# ============================================================
# EXPLAIN PREDICTION
# ============================================================

def explain_prediction(
    profile,
    resume_data=None,
    github_data=None,
    assessment_data=None,
    skill_profile=None
):
    """
    Explain the readiness classification
    using SHAP.
    """

    # --------------------------------------------------------
    # 1. Load trained classifier
    # --------------------------------------------------------

    if not os.path.exists(CLASSIFIER_PATH):
        raise FileNotFoundError(
            f"Model not found: {CLASSIFIER_PATH}"
        )

    classifier = joblib.load(CLASSIFIER_PATH)

    # --------------------------------------------------------
    # 2. Create feature vector
    # --------------------------------------------------------

    features = build_feature_vector(
        profile=profile,
        resume_data=resume_data,
        github_data=github_data,
        assessment_data=assessment_data,
        skill_profile=skill_profile
    )

    # --------------------------------------------------------
    # 3. Create SHAP explainer
    # --------------------------------------------------------

    explainer = shap.TreeExplainer(classifier)

    shap_values = explainer.shap_values(features)

    # --------------------------------------------------------
    # 4. Get model prediction
    # --------------------------------------------------------

    prediction = classifier.predict(features)[0]

    # --------------------------------------------------------
    # 5. Convert SHAP output to 1D feature values
    # --------------------------------------------------------

    if isinstance(shap_values, list):

        # Older SHAP versions
        class_index = list(
            classifier.classes_
        ).index(prediction)

        values = np.asarray(
            shap_values[class_index]
        ).reshape(-1)

    else:

        shap_array = np.asarray(shap_values)

        # ----------------------------------------------------
        # Newer SHAP versions:
        # shape = (samples, features, classes)
        # ----------------------------------------------------

        if shap_array.ndim == 3:

            class_index = list(
                classifier.classes_
            ).index(prediction)

            values = shap_array[
                0,
                :,
                class_index
            ]

        # ----------------------------------------------------
        # shape = (samples, features)
        # ----------------------------------------------------

        elif shap_array.ndim == 2:

            values = shap_array[0]

        # ----------------------------------------------------
        # Already 1D
        # ----------------------------------------------------

        else:

            values = shap_array.reshape(-1)

    # --------------------------------------------------------
    # 6. Safety check
    # --------------------------------------------------------

    if len(values) != len(features.columns):

        raise ValueError(
            f"SHAP feature mismatch: "
            f"{len(values)} SHAP values for "
            f"{len(features.columns)} features."
        )

    # --------------------------------------------------------
    # 7. Create explanation DataFrame
    # --------------------------------------------------------

    explanation = pd.DataFrame({
        "feature": features.columns,
        "impact": values
    })

    # --------------------------------------------------------
    # 8. Absolute impact
    # --------------------------------------------------------

    explanation["absolute_impact"] = (
        explanation["impact"].abs()
    )

    # --------------------------------------------------------
    # 9. Sort by strongest impact
    # --------------------------------------------------------

    explanation = explanation.sort_values(
        "absolute_impact",
        ascending=False
    ).reset_index(drop=True)

    return prediction, explanation


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("SKILLPATH AI - EXPLAINABLE AI")
    print("=" * 60)

    # --------------------------------------------------------
    # Student Profile
    # --------------------------------------------------------

    profile = {
        "cgpa": 8.1
    }

    # --------------------------------------------------------
    # Resume Information
    # --------------------------------------------------------

    resume_data = {
        "skills": [
            "Python",
            "SQL",
            "Git",
            "React",
            "Machine Learning"
        ],

        "skill_count": 5,

        "projects_section": (
            "AI Interview Copilot project"
        )
    }

    # --------------------------------------------------------
    # GitHub Information
    # --------------------------------------------------------

    github_data = {
        "github_repo_count": 12,
        "github_language_count": 5,
        "github_star_count": 20,
        "github_fork_count": 3,
        "github_project_count": 10,
        "github_activity_score": 85
    }

    # --------------------------------------------------------
    # Assessment Information
    # --------------------------------------------------------

    assessment_data = {
        "technical_score": 75,
        "aptitude_score": 70,
        "problem_solving_score": 80,
        "communication_score": 65,
        "interview_confidence_score": 70
    }

    skill_profile = {
        "python": 65,
        "sql": 20,
        "git": 20,
        "problem solving": 20,
        "react": 55,
        "node.js": 45,
        "express.js": 55,
        "mongodb": 45,
        "rest api": 45,
        "machine learning": 65
    }

    # --------------------------------------------------------
    # Run SHAP explanation
    # --------------------------------------------------------

    try:

        prediction, explanation = explain_prediction(
            profile,
            resume_data,
            github_data,
            assessment_data,
            skill_profile
        )

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        print("\nPredicted Readiness Category:")
        print("--------------------------------")

        print(prediction)

        # ----------------------------------------------------
        # Top 10 factors
        # ----------------------------------------------------

        print("\nTop Factors Affecting Prediction:")
        print("--------------------------------")

        top_features = explanation.head(10)

        for _, row in top_features.iterrows():

            feature = row["feature"]
            impact = row["impact"]

            if impact > 0:

                direction = "POSITIVE"

            elif impact < 0:

                direction = "NEGATIVE"

            else:

                direction = "NEUTRAL"

            print(
                f"{feature:<35} "
                f"{impact:>8.4f} "
                f"({direction})"
            )

        # ----------------------------------------------------
        # Full table
        # ----------------------------------------------------

        print("\nComplete SHAP Explanation:")
        print("--------------------------------")

        print(
            explanation[
                [
                    "feature",
                    "impact",
                    "absolute_impact"
                ]
            ].to_string(index=False)
        )

        print("\n" + "=" * 60)
        print("SHAP ANALYSIS COMPLETED")
        print("=" * 60)

    except Exception as error:

        print("\nERROR:")
        print(error)

        print(
            "\nPlease check that:"
        )

        print(
            "1. readiness_classifier.joblib exists"
        )

        print(
            "2. feature_engineering.py is updated"
        )

        print(
            "3. SHAP is installed"
        )