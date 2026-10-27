import os
import sys
import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

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
# IMPORT ML FUNCTIONS
# ============================================================

from predict_readiness import predict_readiness
from explain_prediction import explain_prediction
from resume_parser import analyze_resume
from github_analyzer import analyze_github
from skill_gap import (
    analyze_role,
    create_student_skill_profile
)
from assessment_engine import load_questions, calculate_assessment
from ml.recommendation_engine import (
    generate_skill_recommendations
)
from role_intelligence import (
    find_role,
    search_roles
)


# ============================================================
# IMPORT SCHEMAS
# ============================================================

from backend.schemas import (
    PredictionRequest,
    StudentSettingsUpdate
)
from backend.models import (
    save_student_analysis,
    get_student,
    update_student_settings
)
from backend.auth_routes import router as auth_router


def normalize_assessment_score(score):
    """
    Convert assessment scores to a consistent 0-100 scale.

    Examples:
        8.5  -> 85
        85   -> 85
        100  -> 100
        -5   -> 0
        120  -> 100
    """

    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0.0

    # If score is between 0 and 10,
    # treat it as a 10-point score.
    if 0 <= score <= 10:
        score = score * 10

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return round(score, 2)


# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="SkillPath AI API",
    description=(
        "ML-based Student Career Readiness "
        "and Skill-Gap Analysis API"
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "SkillPath AI API is running",
        "status": "success"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# ROLE INTELLIGENCE
# ============================================================

@app.get("/api/roles/search")
def role_search(
    q: str = "",
    limit: int = 20
):
    """Search available career roles."""

    try:
        limit = max(1, min(limit, 50))
        results = search_roles(
            query=q,
            limit=limit
        )

        return {
            "status": "success",
            "query": q,
            "total": len(results),
            "roles": results
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Role search failed: {error}"
        ) from error


@app.get("/api/roles/requirements")
def get_role_requirements(role: str):
    """Return required skills for a selected career role."""

    if not role.strip():
        raise HTTPException(
            status_code=400,
            detail="Role is required."
        )

    try:
        result = find_role(role)

        if not result["found"]:
            raise HTTPException(
                status_code=404,
                detail=f"Role '{role}' was not found."
            )

        return {
            "status": "success",
            "requested_role": role,
            "role": result["role"],
            "source": result["source"],
            "skills": result["skills"],
            "skill_count": len(result["skills"])
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Role requirements lookup failed: {error}"
        ) from error


# ============================================================
# ASSESSMENT QUESTIONS
# ============================================================

@app.get("/api/assessment/questions")
def get_assessment_questions(
    role: str = "Python Developer",
    difficulty: str | None = None,
):
    try:
        questions = load_questions(
            role=role,
            difficulty=difficulty,
        )

        safe_questions = [
            {
                "id": question["id"],
                "category": question.get("category", "technical"),
                "question": question["question"],
                "options": question["options"],
                "difficulty": question.get("difficulty", "easy"),
            }
            for question in questions
        ]

        return {
            "status": "success",
            "role": role,
            "difficulty": difficulty,
            "total_questions": len(safe_questions),
            "questions": safe_questions,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not load questions: {error}",
        ) from error


# ============================================================
# SUBMIT ASSESSMENT
# ============================================================

@app.post("/api/assessment/submit")
def submit_assessment(data: dict):
    answers = data.get("answers", {})
    question_ids = data.get("question_ids")
    role = data.get("role", "Python Developer")

    if not isinstance(answers, dict):
        raise HTTPException(
            status_code=400,
            detail="Answers must be an object.",
        )

    if not answers:
        raise HTTPException(
            status_code=400,
            detail="Please answer at least one question.",
        )

    if question_ids is not None and not isinstance(
        question_ids, list
    ):
        raise HTTPException(
            status_code=400,
            detail="question_ids must be a list.",
        )

    communication_score = normalize_assessment_score(
        data.get("communication_score", 50)
    )
    confidence_score = normalize_assessment_score(
        data.get("interview_confidence_score", 50)
    )

    try:
        result = calculate_assessment(
            answers=answers,
            communication_score=communication_score,
            interview_confidence_score=confidence_score,
            role=role,
            question_ids=question_ids,
        )

        return {
            "status": "success",
            "assessment": result,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Assessment calculation failed: {error}",
        ) from error


# ============================================================
# READINESS PREDICTION
# ============================================================

@app.post("/api/predict")
def predict(request: PredictionRequest):

    # Convert Pydantic models to dictionaries

    profile = request.profile.model_dump()

    resume_data = request.resume.model_dump()

    github_data = request.github.model_dump()

    assessment_data = request.assessment.model_dump()

    skill_profile = create_student_skill_profile(
        resume_data.get("skills", []),
        resume_data
    )


    # --------------------------------------------------------
    # ML Prediction
    # --------------------------------------------------------

    prediction = predict_readiness(
        profile,
        resume_data,
        github_data,
        assessment_data,
        skill_profile
    )


    # --------------------------------------------------------
    # SHAP Explanation
    # --------------------------------------------------------

    predicted_category, explanation = explain_prediction(
        profile,
        resume_data,
        github_data,
        assessment_data,
        skill_profile
    )


    # --------------------------------------------------------
    # Convert SHAP DataFrame to JSON
    # --------------------------------------------------------

    shap_results = []

    for _, row in explanation.head(10).iterrows():

        shap_results.append({
            "feature": row["feature"],
            "impact": round(
                float(row["impact"]),
                4
            )
        })


    # --------------------------------------------------------
    # Final Response
    # --------------------------------------------------------

    return {

        "status": "success",

        "prediction": {
            "readiness_category":
                prediction["readiness_category"],

            "readiness_score":
                prediction["readiness_score"]
        },

        "explanation": {
            "predicted_category":
                predicted_category,

            "top_factors":
                shap_results
        }
    }


# ============================================================
# RESUME ANALYSIS
# ============================================================

@app.post("/api/resume/analyze")
async def analyze_resume_api(file: UploadFile = File(...)):
    """Upload a resume PDF and analyze it using NLP."""

    filename = file.filename or ""

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        result = analyze_resume(file_bytes=file_bytes)

        return {
            "status": "success",
            "filename": filename,
            "resume_analysis": result
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error


# ============================================================
# COMPLETE STUDENT ANALYSIS
# RESUME PDF + PROFILE + GITHUB + ASSESSMENT
# ============================================================

@app.post("/api/analyze-student")
async def analyze_student(
    name: str = Form(...),
    cgpa: float = Form(...),
    target_role: str = Form(""),
    location: str = Form(""),
    github_url: str = Form(""),
    assessment_json: str = Form(""),
    technical_score: float = Form(0),
    aptitude_score: float = Form(0),
    problem_solving_score: float = Form(0),
    communication_score: float = Form(0),
    interview_confidence_score: float = Form(0),
    file: UploadFile = File(...)
):
    """Analyze a student using a resume, GitHub URL, and assessment data."""

    filename = file.filename or ""

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded resume is empty."
        )

    try:
        resume_data = analyze_resume(file_bytes=file_bytes)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Resume analysis failed: {error}"
        ) from error

    if github_url.strip():
        try:
            github_data = analyze_github(github_url)
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=f"GitHub analysis failed: {error}"
            ) from error
    else:
        github_data = {
            "github_repo_count": 0,
            "github_language_count": 0,
            "github_star_count": 0,
            "github_fork_count": 0,
            "github_project_count": 0,
            "github_activity_score": 0,
            "languages": []
        }

    # --------------------------------------------------
    # COMBINED RESUME + GITHUB SKILL PROFILE
    # --------------------------------------------------

    skill_profile = create_student_skill_profile(
        resume_data.get("skills", []),
        resume_data,
        github_data
    )

    # --------------------------------------------------
    # ROLE ANALYSIS USING RESUME + GITHUB EVIDENCE
    # --------------------------------------------------

    role_analysis = analyze_role(
        target_role,
        resume_data.get("skills", []),
        resume_data,
        github_data
    )

    # --------------------------------------------------
    # Generate personalized recommendations
    # --------------------------------------------------

    recommendations = []

    if "skill_gaps" in role_analysis:
        recommendations = generate_skill_recommendations(
            role_analysis["skill_gaps"]
        )

    profile = {
        "name": name,
        "cgpa": cgpa,
        "target_role": target_role,
        "location": location
    }

    # --------------------------------------------------------
    # ASSESSMENT DATA
    # --------------------------------------------------------

    if assessment_json.strip():

        try:
            assessment_data = json.loads(
                assessment_json
            )

        except json.JSONDecodeError as error:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid assessment JSON: {error}"
            ) from error

    else:

        # Backward compatibility:
        # use manually supplied scores

        assessment_data = {
            "technical_score": technical_score,
            "aptitude_score": aptitude_score,
            "problem_solving_score": problem_solving_score,
            "communication_score": communication_score,
            "interview_confidence_score":
                interview_confidence_score
        }

    # Make sure all five ML features exist

    required_assessment_fields = [
        "technical_score",
        "aptitude_score",
        "problem_solving_score",
        "communication_score",
        "interview_confidence_score"
    ]

    for field in required_assessment_fields:

        if field not in assessment_data:
            assessment_data[field] = 0

        assessment_data[field] = normalize_assessment_score(
            assessment_data[field]
        )

    try:
        prediction = predict_readiness(
            profile,
            resume_data,
            github_data,
            assessment_data,
            skill_profile
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"ML prediction failed: {error}"
        ) from error

    try:
        predicted_category, explanation = explain_prediction(
            profile,
            resume_data,
            github_data,
            assessment_data,
            skill_profile
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"SHAP explanation failed: {error}"
        ) from error

    top_factors = []

    for _, row in explanation.head(10).iterrows():
        impact = float(row["impact"])

        if impact > 0:
            direction = "positive"
        elif impact < 0:
            direction = "negative"
        else:
            direction = "neutral"

        top_factors.append({
            "feature": row["feature"],
            "impact": round(impact, 4),
            "direction": direction
        })

    explanation_data = {
        "predicted_category": predicted_category,
        "top_factors": top_factors
    }

    student_id = save_student_analysis(
        profile=profile,
        resume_analysis=resume_data,
        github_analysis=github_data,
        assessment=assessment_data,
        prediction=prediction,
        explanation=explanation_data,
        role_analysis=role_analysis,
        recommendations=recommendations
    )

    return {
        "status": "success",
        "student_id": student_id,
        "student": {
            "name": name,
            "target_role": target_role,
            "cgpa": cgpa,
            "location": location
        },
        "resume_analysis": {
            "skills": resume_data["skills"],
            "skill_count": resume_data["skill_count"],

            "projects_section": resume_data["projects_section"],
            "project_count": resume_data.get("project_count", 0),

            "experience_section": resume_data["experience_section"],
            "internship_section": resume_data.get("internship_section", ""),
            "internship_count": resume_data.get("internship_count", 0),

            "education_section": resume_data["education_section"],

            "certifications_section": resume_data["certifications_section"],
            "certification_count": resume_data.get("certification_count", 0),

            "experience_months": resume_data.get("experience_months", 0),

            "text_length": resume_data.get("text_length", 0)
        },
        "github_analysis": {
            "github_url": github_url,
            "github_repo_count": github_data["github_repo_count"],
            "github_language_count": github_data["github_language_count"],
            "github_star_count": github_data["github_star_count"],
            "github_fork_count": github_data["github_fork_count"],
            "github_project_count": github_data["github_project_count"],
            "github_activity_score": github_data["github_activity_score"],
            "languages": github_data.get("languages", []),
            "skill_evidence": github_data.get("skill_evidence", {})
        },
        "assessment": assessment_data,
        "prediction": {
            "readiness_category": prediction["readiness_category"],
            "readiness_score": prediction["readiness_score"]
        },
        "explanation": explanation_data,
        "role_analysis": role_analysis,
        "recommendations": recommendations
    }


# ============================================================
# GET STUDENT ANALYSIS
# ============================================================

@app.get("/api/student/{student_id}")
def get_student_analysis(student_id: str):

    try:
        student = get_student(student_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student analysis not found."
            )

        return {
            "status": "success",
            "student": student
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid student ID: {error}"
        ) from error


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@app.get("/api/student/{student_id}/dashboard")
def get_student_dashboard(student_id: str):

    try:

        student = get_student(student_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student dashboard not found."
            )

        profile = student.get("profile", {})
        resume = student.get("resume_analysis", {})
        github = student.get("github_analysis", {})
        assessment = student.get("assessment", {})
        prediction = student.get("prediction", {})
        explanation = student.get("explanation", {})
        role_analysis = student.get(
            "role_analysis",
            {}
        )

        # --------------------------------------------------
        # LOAD SAVED RECOMMENDATIONS
        # --------------------------------------------------

        recommendations = student.get(
            "recommendations",
            []
        )

        # Regenerate recommendations for older records that
        # contain skill gaps but no saved recommendation list.
        if (
            not recommendations
            and role_analysis
            and role_analysis.get("skill_gaps")
        ):
            try:
                recommendations = generate_skill_recommendations(
                    role_analysis["skill_gaps"]
                )

            except Exception as error:
                print(
                    "Recommendation regeneration failed:",
                    error
                )

                recommendations = []

        return {
            "status": "success",

            "student": {
                "id": student_id,
                "name": profile.get("name", ""),
                "cgpa": profile.get("cgpa", 0),
                "target_role": profile.get(
                    "target_role",
                    ""
                ),
                "location": profile.get(
                    "location",
                    ""
                )
            },

            "readiness": {
                "score": prediction.get(
                    "readiness_score",
                    0
                ),
                "category": prediction.get(
                    "readiness_category",
                    "Unknown"
                )
            },

            "resume": {
                "skill_count": resume.get(
                    "skill_count",
                    0
                ),
                "skills": resume.get(
                    "skills",
                    []
                ),
                "project_count": resume.get(
                    "project_count",
                    0
                ),
                "internship_count": resume.get(
                    "internship_count",
                    0
                ),
                "certification_count": resume.get(
                    "certification_count",
                    0
                )
            },

            "github": {
                "github_url": github.get(
                    "github_url",
                    ""
                ),
                "repository_count": github.get(
                    "github_repo_count",
                    0
                ),
                "language_count": github.get(
                    "github_language_count",
                    0
                ),
                "stars": github.get(
                    "github_star_count",
                    0
                ),
                "forks": github.get(
                    "github_fork_count",
                    0
                ),
                "project_count": github.get(
                    "github_project_count",
                    0
                ),
                "activity_score": github.get(
                    "github_activity_score",
                    0
                ),
                "languages": github.get(
                    "languages",
                    []
                ),
                "skill_evidence": github.get(
                    "skill_evidence",
                    {}
                )
            },

            "assessment": {
                "technical_score": assessment.get(
                    "technical_score",
                    0
                ),
                "aptitude_score": assessment.get(
                    "aptitude_score",
                    0
                ),
                "problem_solving_score": assessment.get(
                    "problem_solving_score",
                    0
                ),
                "communication_score": assessment.get(
                    "communication_score",
                    0
                ),
                "interview_confidence_score": assessment.get(
                    "interview_confidence_score",
                    0
                )
            },

            "explanation": explanation,

            "role_analysis": role_analysis,

            "recommendations": recommendations
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Dashboard loading failed: {error}"
        ) from error


# ============================================================
# UPDATE STUDENT SETTINGS
# ============================================================

@app.put("/api/student/{student_id}/settings")
def update_student_settings_api(
    student_id: str,
    settings: StudentSettingsUpdate
):
    try:
        student = get_student(student_id)

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found."
            )

        updates = settings.model_dump(exclude_unset=True)

        for field, value in updates.items():
            if value is not None:
                cleaned_value = value.strip()

                if field in {"name", "target_role"} and not cleaned_value:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{field.replace('_', ' ').capitalize()} cannot be empty."
                    )

                updates[field] = cleaned_value

        updated_student = update_student_settings(
            student_id=student_id,
            **updates
        )

        if not updated_student:
            raise HTTPException(
                status_code=404,
                detail="Unable to update student settings."
            )

        return {
            "status": "success",
            "message": "Settings updated successfully.",
            "student": updated_student
        }

    except HTTPException:
        raise

    except Exception as error:
        print("SETTINGS UPDATE ERROR:", error)
        raise HTTPException(
            status_code=500,
            detail=f"Settings update failed: {error}"
        ) from error