from pydantic import BaseModel, Field
from typing import List, Optional


class StudentProfile(BaseModel):
    name: str
    cgpa: float = Field(ge=0, le=10)
    target_role: Optional[str] = None
    location: Optional[str] = None


class ResumeData(BaseModel):
    skills: List[str] = []
    skill_count: int = 0
    projects_section: str = ""
    experience_section: str = ""
    education_section: str = ""
    certifications_section: str = ""


class GithubData(BaseModel):
    github_repo_count: int = 0
    github_language_count: int = 0
    github_star_count: int = 0
    github_fork_count: int = 0
    github_project_count: int = 0
    github_activity_score: float = 0


class AssessmentData(BaseModel):
    technical_score: float = Field(ge=0, le=100)
    aptitude_score: float = Field(ge=0, le=100)
    problem_solving_score: float = Field(ge=0, le=100)
    communication_score: float = Field(ge=0, le=100)
    interview_confidence_score: float = Field(ge=0, le=100)


class PredictionRequest(BaseModel):
    profile: StudentProfile
    resume: ResumeData
    github: GithubData
    assessment: AssessmentData


class StudentSettingsUpdate(BaseModel):
    name: Optional[str] = None
    target_role: Optional[str] = None
    location: Optional[str] = None