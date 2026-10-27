import os
from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

# ============================================================
# MONGODB CONNECTION
# ============================================================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

client = MongoClient(MONGO_URI)

db = client["skillpath_ai"]

students_collection = db["students"]
analysis_collection = db["analysis"]

# ============================================================
# SAVE STUDENT ANALYSIS
# ============================================================

def save_student_analysis(
    profile,
    resume_analysis,
    github_analysis,
    assessment,
    prediction,
    explanation,
    role_analysis=None,
    recommendations=None
):
    """
    Save complete student analysis into MongoDB.
    """

    document = {
        "profile": profile,

        "resume_analysis": resume_analysis,

        "github_analysis": github_analysis,

        "assessment": assessment,

        "prediction": prediction,

        "explanation": explanation,

        "role_analysis": role_analysis or {},

        "recommendations": recommendations or [],

        "created_at": datetime.utcnow()
    }

    result = students_collection.insert_one(document)

    student_id = str(result.inserted_id)

    return student_id

# ============================================================
# GET STUDENT
# ============================================================

def get_student(student_id):
    """
    Get student analysis using MongoDB ObjectId.
    """

    try:
        object_id = ObjectId(student_id)
    except Exception:
        return None

    student = students_collection.find_one({
        "_id": object_id
    })

    if not student:
        return None

    # Convert MongoDB ObjectId to string
    student["_id"] = str(student["_id"])

    return student


# ============================================================
# UPDATE STUDENT SETTINGS
# ============================================================

def update_student_settings(
    student_id,
    name=None,
    target_role=None,
    location=None
):
    """Update editable profile settings for a saved student."""

    try:
        object_id = ObjectId(student_id)
    except Exception:
        return None

    update_fields = {}

    if name is not None:
        update_fields["profile.name"] = name

    if target_role is not None:
        update_fields["profile.target_role"] = target_role

    if location is not None:
        update_fields["profile.location"] = location

    if not update_fields:
        return get_student(student_id)

    result = students_collection.update_one(
        {"_id": object_id},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        return None

    return get_student(student_id)