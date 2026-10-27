import json
import os
import re

# --------------------------------------------------
# 1. Load role-skill requirements
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ROLE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "role_skills.json"
)


def load_role_skills():
    """Load role requirements from role_skills.json."""

    with open(ROLE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# 2. Normalize skill names
# --------------------------------------------------

def normalize_skill(skill):
    """Normalize skill names for comparison."""

    skill = str(skill).lower().strip()

    aliases = {
        # Programming languages
        "python": "python",
        "java": "java",
        "javascript": "javascript",
        "js": "javascript",
        "typescript": "typescript",
        "ts": "typescript",
        "c++": "c++",
        "cpp": "c++",
        "c": "c",
        "c#": "c#",
        "go": "go",
        "rust": "rust",
        "dart": "dart",

        # Frontend
        "html": "html",
        "css": "css",
        "react.js": "react",
        "reactjs": "react",
        "react": "react",
        "angular": "angular",
        "vue": "vue",
        "next.js": "next.js",
        "nextjs": "next.js",
        "figma": "figma",
        "ui ux": "ui ux",
        "ui/ux": "ui ux",

        # Backend
        "node": "node.js",
        "nodejs": "node.js",
        "node.js": "node.js",
        "express": "express.js",
        "expressjs": "express.js",
        "express.js": "express.js",
        "django": "django",
        "flask": "flask",
        "fastapi": "fastapi",
        "spring boot": "spring",
        "spring": "spring",

        # Database
        "mysql": "sql",
        "sql": "sql",
        "postgresql": "sql",
        "postgres": "sql",
        "sqlite": "sql",
        "mongodb": "mongodb",
        "mongo": "mongodb",
        "redis": "redis",
        "kafka": "kafka",

        # API
        "rest": "rest api",
        "rest api": "rest api",
        "rest apis": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",

        # Git / DevOps
        "git": "git",
        "github": "github",
        "docker": "docker",
        "kubernetes": "kubernetes",
        "terraform": "terraform",
        "jenkins": "jenkins",
        "linux": "linux",
        "aws": "aws",
        "azure": "azure",
        "gcp": "gcp",

        # Machine Learning / AI
        "ml": "machine learning",
        "machine learning": "machine learning",
        "deep learning": "deep learning",
        "tensorflow": "tensorflow",
        "pytorch": "pytorch",
        "nlp": "nlp",
        "computer vision": "computer vision",
        "sklearn": "scikit-learn",
        "scikit learn": "scikit-learn",
        "scikit-learn": "scikit-learn",

        # Data / BI
        "pandas": "pandas",
        "numpy": "numpy",
        "power bi": "power bi",
        "tableau": "tableau",
        "excel": "excel",

        # Problem solving
        "dsa": "problem solving",
        "data structures": "problem solving",
        "algorithms": "problem solving",
        "problem solving": "problem solving",

        # Cloud / DevOps synonyms
        "cloud": "cloud",
        "networking": "networking",
        "ci/cd": "ci/cd",
        "devops": "devops",
        "sre": "sre",
        "site reliability engineering": "sre"
    }

    return aliases.get(skill, skill)


# --------------------------------------------------
# 3. Create student skill profile
# --------------------------------------------------

def normalize_skill_name(skill):
    """
    Normalize different names of the same skill.
    """

    if not skill:
        return ""

    skill = str(skill).strip().lower()

    skill_aliases = {
        "python": "python",
        "java": "java",
        "javascript": "javascript",
        "js": "javascript",
        "typescript": "typescript",
        "ts": "typescript",
        "html": "html",
        "html5": "html",
        "css": "css",
        "css3": "css",
        "react": "react",
        "reactjs": "react",
        "react.js": "react",
        "angular": "angular",
        "vue": "vue",
        "next.js": "next.js",
        "nextjs": "next.js",
        "node": "node.js",
        "nodejs": "node.js",
        "node.js": "node.js",
        "express": "express.js",
        "expressjs": "express.js",
        "express.js": "express.js",
        "django": "django",
        "flask": "flask",
        "fastapi": "fastapi",
        "spring": "spring",
        "spring boot": "spring",
        "mysql": "sql",
        "postgresql": "sql",
        "postgres": "sql",
        "sqlite": "sql",
        "sql": "sql",
        "mongodb": "mongodb",
        "mongo": "mongodb",
        "redis": "redis",
        "kafka": "kafka",
        "git": "git",
        "github": "github",
        "docker": "docker",
        "kubernetes": "kubernetes",
        "terraform": "terraform",
        "jenkins": "jenkins",
        "linux": "linux",
        "aws": "aws",
        "azure": "azure",
        "gcp": "gcp",
        "rest": "rest api",
        "rest api": "rest api",
        "restful api": "rest api",
        "machine learning": "machine learning",
        "machine-learning": "machine learning",
        "ml": "machine learning",
        "deep learning": "deep learning",
        "tensorflow": "tensorflow",
        "pytorch": "pytorch",
        "nlp": "nlp",
        "computer vision": "computer vision",
        "scikit-learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "pandas": "pandas",
        "numpy": "numpy",
        "power bi": "power bi",
        "tableau": "tableau",
        "excel": "excel",
        "figma": "figma",
        "ui ux": "ui ux",
        "ui/ux": "ui ux",
        "data structures": "problem solving",
        "algorithms": "problem solving",
        "dsa": "problem solving",
        "problem solving": "problem solving",
        "c++": "c++",
        "cpp": "c++",
        "dart": "dart",
        "c#": "c#",
        "go": "go",
        "rust": "rust",
    }

    return skill_aliases.get(skill, skill)


def create_student_skill_profile(
    resume_skills,
    resume_data=None,
    github_data=None
):
    """
    Create a combined student skill profile using:

    1. Resume evidence
    2. GitHub evidence

    GitHub evidence is treated as supporting evidence.
    It does NOT replace resume evidence.
    """

    resume_data = resume_data or {}
    github_data = github_data or {}

    skill_profile = {}

    # ==================================================
    # BUILD RESUME TEXT
    # ==================================================

    project_text = str(
        resume_data.get(
            "projects_section",
            resume_data.get("projects", "")
        )
    ).lower()

    internship_text = str(
        resume_data.get(
            "internship_section",
            resume_data.get("internships", "")
        )
    ).lower()

    experience_text = str(
        resume_data.get(
            "experience_section",
            resume_data.get("experience", "")
        )
    ).lower()

    certification_text = str(
        resume_data.get(
            "certifications_section",
            resume_data.get("certifications", "")
        )
    ).lower()

    # ==================================================
    # RESUME SKILL EVIDENCE
    # ==================================================

    for skill in resume_skills or []:
        skill_name = normalize_skill_name(skill)

        if not skill_name:
            continue

        # Base evidence from resume
        score = 20

        # Project evidence
        if skill_name.lower() in project_text:
            score += 25

        # Internship evidence
        if skill_name.lower() in internship_text:
            score += 25

        # Experience evidence
        if skill_name.lower() in experience_text:
            score += 15

        # Certification evidence
        if skill_name.lower() in certification_text:
            score += 10

        skill_profile[skill_name] = min(
            100,
            score
        )

    # ==================================================
    # GITHUB SKILL EVIDENCE
    # ==================================================

    github_evidence = github_data.get(
        "skill_evidence",
        {}
    )

    for skill, github_score in github_evidence.items():
        normalized_skill = normalize_skill_name(skill)

        if not normalized_skill:
            continue

        try:
            github_score = float(github_score)
        except (TypeError, ValueError):
            github_score = 0

        # GitHub is supporting evidence.
        # We give only 40% weight to GitHub evidence.
        github_bonus = github_score * 0.40

        if normalized_skill in skill_profile:
            # Resume evidence + GitHub supporting evidence
            combined_score = (
                skill_profile[normalized_skill]
                + github_bonus
            )

            skill_profile[normalized_skill] = min(
                100,
                round(combined_score)
            )

        else:
            # GitHub-only skill gets limited evidence.
            skill_profile[normalized_skill] = min(
                40,
                round(github_bonus)
            )

    return skill_profile


def calculate_role_alignment(
    student_skills,
    role_requirements
):
    """
    Calculate alignment between student skills
    and a selected role.
    """

    if not role_requirements:
        return 0

    total_weight = sum(role_requirements.values())

    matched_weight = 0

    for required_skill, weight in role_requirements.items():

        required_normalized = normalize_skill(
            required_skill
        )

        student_level = student_skills.get(
            required_normalized,
            0
        )

        # Student evidence is capped at 100.
        student_level = min(
            max(student_level, 0),
            100
        )

        matched_weight += (
            student_level / 100
        ) * weight

    alignment = (
        matched_weight / total_weight
    ) * 100

    return round(alignment, 2)


# --------------------------------------------------
# 5. Find skill gaps
# --------------------------------------------------

def find_skill_gaps(
    student_skills,
    role_requirements
):
    """
    Find skills required by the selected role
    that are missing from the student's resume.
    """

    gaps = []

    for required_skill, required_score in role_requirements.items():

        normalized = normalize_skill(
            required_skill
        )

        student_score = student_skills.get(
            normalized,
            0
        )

        gap = max(
            required_score - student_score,
            0
        )

        if gap > 0:

            gaps.append({
                "skill": required_skill,
                "required_score": required_score,
                "student_score": student_score,
                "gap": gap
            })

    gaps.sort(
        key=lambda item: item["gap"],
        reverse=True
    )

    return gaps


# --------------------------------------------------
# 6. Normalize role names before matching
# --------------------------------------------------

def normalize_role_name(role):
    """Normalize common role spelling variations before matching."""

    if role is None:
        return ""

    normalized = str(role).strip().lower()
    normalized = re.sub(r"[-_]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)

    role_aliases = {
        "software developer": "software developer",
        "software dev": "software developer",
        "software devloper": "software developer",
        "software engineer": "software developer",
        "software eng": "software developer",
        "sde": "software developer",
        "sde 1": "software developer",
        "sde i": "software developer",

        "frontend developer": "frontend developer",
        "frontend devloper": "frontend developer",
        "front end developer": "frontend developer",
        "front end devloper": "frontend developer",
        "front-end developer": "frontend developer",
        "front-end devloper": "frontend developer",
        "frontend dev": "frontend developer",
        "web developer": "frontend developer",

        "backend developer": "backend developer",
        "backend devloper": "backend developer",
        "back end developer": "backend developer",
        "back end devloper": "backend developer",
        "back-end developer": "backend developer",
        "back-end devloper": "backend developer",
        "backend dev": "backend developer",

        "full stack developer": "full stack developer",
        "fullstack developer": "full stack developer",
        "full stack devloper": "full stack developer",
        "fullstack devloper": "full stack developer",

        "python developer": "python developer",
        "python devloper": "python developer",
        "python dev": "python developer",

        "java developer": "java developer",
        "java devloper": "java developer",
        "java dev": "java developer",

        "data analyst": "data analyst",
        "data analist": "data analyst",

        "data scientist": "data scientist",
        "data scientest": "data scientist",

        "ml engineer": "ml engineer",
        "ml enginer": "ml engineer",

        "cloud engineer": "cloud engineer",
        "cloud enginer": "cloud engineer",
        "aws cloud engineer": "aws cloud engineer",
        "azure cloud engineer": "azure cloud engineer",
        "gcp cloud engineer": "gcp cloud engineer",
        "devops engineer": "devops engineer",
        "site reliability engineer": "site reliability engineer",
        "platform engineer": "platform engineer",
        "cloud architect": "cloud architect",
        "devsecops engineer": "devsecops engineer",
        "security engineer": "security engineer",
        "cybersecurity analyst": "cybersecurity analyst",
        "cybersecurity engineer": "cybersecurity engineer",
        "soc analyst": "soc analyst",
        "cloud security engineer": "cloud security engineer",
        "application security engineer": "application security engineer",
        "penetration tester": "penetration tester",
        "qa engineer": "qa engineer",
        "software tester": "software tester",
        "automation tester": "automation tester",
        "sdet": "sdet",
        "performance test engineer": "performance test engineer",
        "database administrator": "database administrator",
        "database developer": "database developer",
        "sql developer": "sql developer",
        "mongodb developer": "mongodb developer",
        "data warehouse engineer": "data warehouse engineer",
        "ui designer": "ui designer",
        "ux designer": "ux designer",
        "ui ux designer": "ui ux designer",
        "product designer": "product designer",
        "product manager": "product manager",
        "business analyst": "business analyst",
        "technical product manager": "technical product manager",
        "ai engineer": "ai engineer",
        "ai ml engineer": "ai engineer",
        "ml engineer": "ml engineer",
        "deep learning engineer": "deep learning engineer",
        "nlp engineer": "nlp engineer",
        "computer vision engineer": "computer vision engineer",
        "data engineer": "data engineer",
        "bi analyst": "bi analyst",
        "analytics engineer": "analytics engineer",
        "mobile app developer": "mobile app developer",
        "android developer": "android developer",
        "ios developer": "ios developer",
        "flutter developer": "flutter developer",
        "react developer": "react developer",
        "angular developer": "angular developer",
        "node.js developer": "node.js developer"
    }

    return role_aliases.get(normalized, normalized)


# --------------------------------------------------
# 7. Analyze selected role
# --------------------------------------------------

def analyze_role(
    target_role,
    resume_skills,
    resume_data=None,
    github_data=None
):
    """
    Analyze the student's selected career role.
    """

    roles = load_role_skills()
    original_role = str(target_role).strip()
    normalized_role = normalize_role_name(target_role)

    role_lookup = {}

    for role_name in roles.keys():
        exact_key = str(role_name).strip().lower()
        role_lookup[exact_key] = role_name

        normalized_key = normalize_role_name(role_name)

        if normalized_key == "software developer":
            role_lookup[normalized_key] = "software developer"
        elif normalized_key not in role_lookup:
            role_lookup[normalized_key] = role_name

    selected_role = role_lookup.get(normalized_role)

    if selected_role is None:
        try:
            from role_intelligence import find_role
            intelligence = find_role(original_role)
        except Exception:
            intelligence = {
                "found": False,
                "role": original_role,
                "skills": {}
            }

        return {
            "role": original_role,
            "error": "Role not found in local catalog.",
            "role_found": False,
            "role_intelligence": intelligence,
            "skill_gaps": [],
            "available_roles": list(roles.keys())
        }

    role_requirements = roles[selected_role]

    student_skills = create_student_skill_profile(
        resume_skills,
        resume_data,
        github_data
    )

    alignment = calculate_role_alignment(
        student_skills,
        role_requirements
    )

    gaps = find_skill_gaps(
        student_skills,
        role_requirements
    )

    return {
        "role": selected_role,
        "role_requirements": role_requirements,
        "student_skills": student_skills,
        "role_alignment": alignment,
        "skill_gaps": gaps
    }


# --------------------------------------------------
# 7. Test
# --------------------------------------------------

if __name__ == "__main__":

    test_resume_skills = [
        "Python",
        "Java",
        "JavaScript",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "Express.js",
        "MongoDB",
        "MySQL",
        "Git",
        "GitHub",
        "REST API",
        "Machine Learning",
        "Scikit-learn",
        "Pandas",
        "Data Structures"
    ]

    test_resume_data = {
        "projects_section": """
        AI Interview Copilot | AI-Powered Interview Preparation Platform

        Tech Stack:
        React.js, JavaScript, Node.js, Express.js, MongoDB,
        Python, REST APIs, Groq AI, Firebase, JWT, Tailwind CSS

        Developed a full-stack AI-powered interview preparation platform.
        Implemented AI-powered resume analysis and interview features.

        Sonic Sorter Music | Music Genre Classification Application

        Tech Stack:
        Python, Pandas, Scikit-learn, Random Forest, Machine Learning

        Developed a Python-based machine learning application.

        Flutter Restaurant App

        Tech Stack:
        Flutter, Dart, UI/UX Design, Responsive Design
        """,

        "internship_section": "",

        "experience_section": "",

        "certifications_section": """
        Advanced Python Programming and Applied Machine Learning
        Full Stack Java Development
        UI/UX + HTML
        """
    }

    test_github_data = {
        "skill_evidence": {
            "javascript": 80,
            "c++": 40,
            "css": 40,
            "dart": 40,
            "jupyter notebook": 40,
            "python": 20,
            "machine learning": 20
        }
    }

    result = analyze_role(
        "Backend Developer",
        test_resume_skills,
        test_resume_data,
        test_github_data
    )

    print("\n===================================")
    print("       SKILL GAP ANALYSIS")
    print("===================================")

    print("\nRole:")
    print(result["role"])

    print("\nStudent Skills:")
    for skill, score in result["student_skills"].items():
        print(f"- {skill}: {score}")

    print("\nRole Alignment:")
    print(f"{result['role_alignment']}%")

    print("\nSkill Gaps:")
    for gap in result["skill_gaps"]:
        print(
            f"- {gap['skill']} "
            f"(Required: {gap['required_score']}, "
            f"Student: {gap['student_score']}, "
            f"Gap: {gap['gap']})"
        )
