import json
import os
import re


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ROLE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "role_skills.json"
)


# ============================================================
# NORMALIZE ROLE
# ============================================================

def normalize_role(role):

    if not role:
        return ""

    role = str(role).strip().lower()

    # Replace -, _, / with spaces
    role = re.sub(
        r"[-_/]+",
        " ",
        role
    )

    # Remove extra spaces
    role = re.sub(
        r"\s+",
        " ",
        role
    )

    return role


# ============================================================
# ROLE ALIASES
# ============================================================

ROLE_ALIASES = {

    # --------------------------------------------------------
    # SOFTWARE DEVELOPMENT
    # --------------------------------------------------------

    "software developer": "software developer",
    "software dev": "software developer",
    "software devloper": "software developer",
    "software engineer": "Software Engineer",
    "software engineering": "Software Engineer",
    "sde": "Software Engineer",
    "sde 1": "Software Engineer",
    "sde i": "Software Engineer",

    "frontend developer": "frontend developer",
    "frontend engineer": "Frontend Developer",
    "front end developer": "frontend developer",

    "backend developer": "backend developer",
    "back end developer": "backend developer",
    "backend engineer": "Backend Developer",
    "server side developer": "Backend Developer",

    "full stack developer": "full stack developer",
    "fullstack developer": "Full Stack Developer",
    "full stack engineer": "Full Stack Developer",

    "python developer": "python developer",
    "python engineer": "Python Developer",

    "java developer": "java developer",
    "java engineer": "Java Developer",

    "node developer": "Node.js Developer",
    "node js developer": "Node.js Developer",
    "node.js developer": "node.js developer",

    "react engineer": "React Developer",
    "react developer": "react developer",
    "react js developer": "React Developer",
    "react.js developer": "react developer",
    "angular engineer": "Angular Developer",
    "angular js developer": "Angular Developer",
    "flutter engineer": "Flutter Developer",
    "android engineer": "Android Developer",
    "ios engineer": "iOS Developer",

    # --------------------------------------------------------
    # DATA / AI
    # --------------------------------------------------------

    "data analyst": "data analyst",
    "data analytics": "data analyst",
    "data analyst role": "data analyst",

    "data scientist": "data scientist",
    "data science": "data scientist",

    "machine learning engineer": "ml engineer",
    "ml engineer": "ml engineer",
    "machine learning developer": "ml engineer",

    "ai engineer": "ai engineer",
    "ai ml engineer": "AI/ML Engineer",
    "artificial intelligence engineer": "ai engineer",
    "artificial intelligence developer": "AI Engineer",
    "ai developer": "ai engineer",

    "deep learning engineer": "deep learning engineer",
    "deep learning developer": "Deep Learning Engineer",

    "nlp engineer": "nlp engineer",
    "natural language processing engineer": "nlp engineer",

    "computer vision engineer": "computer vision engineer",
    "computer vision developer": "Computer Vision Engineer",

    "data engineer": "data engineer",
    "data engineering": "Data Engineer",
    "business intelligence analyst": "BI Analyst",

    # --------------------------------------------------------
    # CLOUD / DEVOPS
    # --------------------------------------------------------

    "cloud engineer": "cloud engineer",
    "cloud developer": "cloud engineer",

    "aws engineer": "aws cloud engineer",
    "aws developer": "AWS Cloud Engineer",
    "aws cloud engineer": "aws cloud engineer",

    "azure engineer": "azure cloud engineer",
    "azure developer": "Azure Cloud Engineer",
    "azure cloud engineer": "azure cloud engineer",

    "gcp engineer": "gcp cloud engineer",
    "gcp developer": "GCP Cloud Engineer",
    "google cloud engineer": "gcp cloud engineer",

    "devops engineer": "devops engineer",
    "devops": "DevOps Engineer",

    "site reliability engineer": "site reliability engineer",
    "sre": "site reliability engineer",

    "cloud architect": "cloud architect",
    "platform engineer": "Platform Engineer",
    "devsecops": "DevSecOps Engineer",

    # --------------------------------------------------------
    # CYBERSECURITY
    # --------------------------------------------------------

    "cybersecurity analyst": "cybersecurity analyst",
    "cyber security analyst": "cybersecurity analyst",
    "security analyst": "Cybersecurity Analyst",

    "cybersecurity engineer": "cybersecurity engineer",
    "cyber security engineer": "cybersecurity engineer",

    "security engineer": "security engineer",

    "soc analyst": "soc analyst",

    "penetration tester": "penetration tester",
    "pen tester": "penetration tester",
    "penetration testing": "Penetration Tester",

    "cloud security engineer": "Cloud Security Engineer",
    "application security engineer": "Application Security Engineer",

    # --------------------------------------------------------
    # TESTING
    # --------------------------------------------------------

    "qa engineer": "qa engineer",
    "quality assurance engineer": "qa engineer",
    "qa tester": "QA Engineer",

    "software tester": "software tester",
    "software test engineer": "Software Tester",

    "automation tester": "automation tester",

    "test automation engineer": "automation tester",
    "automation test engineer": "Automation Tester",

    "sdet": "sdet",
    "software development engineer in test": "SDET",

    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    "database administrator": "database administrator",
    "dba": "database administrator",
    "database admin": "Database Administrator",

    "database developer": "database developer",

    "sql developer": "sql developer",
    "sql engineer": "SQL Developer",
    "mongodb engineer": "MongoDB Developer",
    "data warehouse engineer": "Data Warehouse Engineer",

    # --------------------------------------------------------
    # MOBILE
    # --------------------------------------------------------

    "android developer": "android developer",

    "ios developer": "ios developer",

    "mobile app developer": "mobile app developer",

    "flutter developer": "flutter developer",

    # --------------------------------------------------------
    # DESIGN
    # --------------------------------------------------------

    "ui designer": "ui designer",

    "ux designer": "ux designer",

    "ui ux designer": "ui ux designer",

    "ui/ux designer": "ui ux designer",

    "product designer": "product designer",

    # --------------------------------------------------------
    # PRODUCT / BUSINESS
    # --------------------------------------------------------

    "product manager": "product manager",

    "technical product manager": "technical product manager",

    "business analyst": "business analyst",

    "business intelligence analyst": "bi analyst",

    "bi analyst": "bi analyst"
}


# ============================================================
# LOAD ROLE SKILLS
# ============================================================

def load_role_skills():

    if not os.path.exists(ROLE_FILE):

        raise FileNotFoundError(
            f"Role skills file not found: {ROLE_FILE}"
        )

    with open(
        ROLE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# FIND ROLE
# ============================================================

def find_role(target_role):

    roles = load_role_skills()

    normalized_target = normalize_role(
        target_role
    )

    # Resolve aliases before comparing with the catalog.
    canonical_role = ROLE_ALIASES.get(
        normalized_target,
        normalized_target
    )
    normalized_canonical_role = normalize_role(canonical_role)

    # Check available roles
    for role_name, skills in roles.items():

        normalized_role = normalize_role(
            role_name
        )

        if normalized_role == normalized_canonical_role:

            return {
                "found": True,
                "role": role_name,
                "skills": skills,
                "source": "role_catalog",
                "canonical_role": canonical_role
            }

    # Role not found
    return {
        "found": False,
        "role": target_role,
        "canonical_role": canonical_role,
        "skills": {},
        "source": None
    }


def search_roles(query="", limit=20):
    """Search catalog role names and aliases that resolve to catalog roles."""

    roles = load_role_skills()
    normalized_query = normalize_role(query)
    results = []
    seen_roles = set()

    for role_name in roles:
        normalized_role = normalize_role(role_name)

        if not normalized_query or normalized_query in normalized_role:
            results.append({"role": role_name})
            seen_roles.add(normalized_role)

    if normalized_query:
        for alias, canonical_role in ROLE_ALIASES.items():
            normalized_alias = normalize_role(alias)
            normalized_canonical_role = normalize_role(canonical_role)

            if normalized_query not in normalized_alias:
                continue

            for role_name in roles:
                normalized_role = normalize_role(role_name)
                if (
                    normalized_role == normalized_canonical_role
                    and normalized_role not in seen_roles
                ):
                    results.append({"role": alias.title()})
                    seen_roles.add(normalized_role)
                    break

    return results[:limit]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_roles = [
        "Software Developer",
        "Software Engineer",
        "SDE",
        "SDE 1",
        "Backend Engineer",
        "Frontend Engineer",
        "Fullstack Developer",
        "Python Engineer",
        "Java Engineer",
        "Machine Learning Engineer",
        "AI Engineer",
        "Data Science",
        "AWS Engineer",
        "DevOps",
        "SRE",
        "Cyber Security Analyst",
        "SOC Analyst",
        "QA Tester",
        "Automation Test Engineer",
        "DBA"
    ]

    print("=" * 60)
    print("SKILLPATH AI - ROLE INTELLIGENCE TEST")
    print("=" * 60)

    for role in test_roles:

        result = find_role(role)

        print()
        print("Input Role :", role)
        print("Found      :", result["found"])
        print("Matched    :", result["role"])
        print("Canonical  :", result["canonical_role"])
        print("Source     :", result["source"])

        if result["found"]:

            print(
                "Skills     :",
                len(result["skills"])
            )

    print()
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

    print()
    print("SEARCH 'machine':", search_roles("machine"))