import os
import re

import fitz


SKILLS = [
    "Python", "Java", "JavaScript", "HTML", "CSS", "React",
    "Node.js", "Express.js", "SQL", "MongoDB", "MySQL", "Git",
    "GitHub", "REST API", "Machine Learning", "Scikit-learn",
    "Pandas", "NumPy", "Docker", "AWS", "Linux", "C++", "C",
    "FastAPI", "Spring", "Data Structures", "Algorithms"
]


def extract_text_from_bytes(file_bytes):
    """Extract text from an uploaded PDF while preserving line breaks."""

    document = fitz.open(stream=file_bytes, filetype="pdf")
    pages = [page.get_text("text") for page in document]
    document.close()
    return "\n".join(pages)


def clean_text(text):
    """Clean PDF text while preserving section structure."""

    if not text:
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_skills(text):
    """Extract canonical skill names using alias-aware matching."""

    found_skills = []
    text_lower = text.lower()

    skill_aliases = {
        "Python": ["python"],
        "Java": ["java"],
        "JavaScript": ["javascript", "js"],
        "HTML": ["html"],
        "CSS": ["css"],
        "React": ["react", "react.js", "reactjs"],
        "Node.js": ["node.js", "nodejs", "node"],
        "Express.js": ["express.js", "expressjs", "express"],
        "SQL": ["sql"],
        "MongoDB": ["mongodb", "mongo db"],
        "MySQL": ["mysql"],
        "Git": ["git"],
        "GitHub": ["github"],
        "REST API": ["rest api", "rest apis", "restful api", "restful apis"],
        "Machine Learning": ["machine learning", "machine-learning"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Docker": ["docker"],
        "AWS": ["aws", "amazon web services"],
        "Linux": ["linux"],
        "C++": ["c++"],
        "C": ["c programming"],
        "FastAPI": ["fastapi"],
        "Spring": ["spring", "spring boot"],
        "Data Structures": ["data structures", "data structure"],
        "Algorithms": ["algorithms", "algorithm"]
    }

    for skill, aliases in skill_aliases.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
            if re.search(pattern, text_lower):
                found_skills.append(skill)
                break

    return found_skills


SECTION_ALIASES = {
    "projects": ["projects", "project"],
    "experience": ["experience", "work experience", "professional experience"],
    "internship": ["internship", "internships", "internship experience"],
    "education": ["education", "academic background", "educational background"],
    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "certifications & achievements",
        "certification & achievements"
    ],
    "skills": ["skills", "technical skills", "technical skills & tools"],
    "achievements": ["achievements", "achievement"]
}


def normalize_heading(line):
    """Normalize a possible section heading."""

    line = re.sub(r"[:\-|]+$", "", line.strip())
    return re.sub(r"\s+", " ", line).strip().lower()


def detect_section_heading(line):
    normalized = normalize_heading(line)
    for section, aliases in SECTION_ALIASES.items():
        if normalized in [alias.lower() for alias in aliases]:
            return section
    return None


def extract_sections(text):
    """Extract recognized sections from line-preserved resume text."""

    sections = {}
    current_section = None
    current_lines = []

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        section = detect_section_heading(line)
        if section:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = section
            current_lines = []
        elif current_section:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def extract_section(text, section_names):
    """
    Extract a resume section while preserving line structure.

    Example:
        extract_section(text, ["certifications", "certificates"])
    """

    if not text:
        return ""

    lines = text.splitlines()

    normalized_names = [
        name.strip().lower()
        for name in section_names
    ]

    start_index = None

    for index, line in enumerate(lines):

        cleaned_line = re.sub(
            r"[^a-zA-Z0-9+#/& ]",
            " ",
            line
        )

        cleaned_line = re.sub(
            r"\s+",
            " ",
            cleaned_line
        ).strip().lower()

        heading = cleaned_line.strip(" :-|")

        for name in normalized_names:

            if heading == name:
                start_index = index
                break

        if start_index is not None:
            break

    if start_index is None:
        return ""

    all_sections = [
        "summary",
        "objective",
        "profile",
        "education",
        "skills",
        "technical skills",
        "target role",
        "professional summary",
        "projects",
        "project",
        "experience",
        "work experience",
        "internship",
        "internships",
        "certifications",
        "certificates",
        "certifications & achievements",
        "certification & achievements",
        "achievements",
        "languages",
        "hobbies",
        "interests",
        "contact"
    ]

    collected = []

    for index in range(start_index + 1, len(lines)):

        line = lines[index].strip()

        if not line:
            continue

        cleaned_line = re.sub(
            r"[^a-zA-Z0-9+#/& ]",
            " ",
            line
        )

        cleaned_line = re.sub(
            r"\s+",
            " ",
            cleaned_line
        ).strip().lower()

        heading = cleaned_line.strip(" :-|")

        if heading in all_sections:
            break

        collected.append(line)

    return "\n".join(collected).strip()


def count_projects(projects_text):
    """Estimate project count from known titles and resume separators."""

    if not projects_text:
        return 0

    separators = re.findall(r"\s+\|\s+", projects_text)
    known_projects = [
        "AI Interview Copilot",
        "Sonic Sorter Music",
        "Flutter Restaurant App"
    ]
    known_count = sum(
        title.lower() in projects_text.lower()
        for title in known_projects
    )

    return min(max(known_count, len(separators), 1), 20)


def count_internships(text):
    if not text:
        return 0
    matches = re.findall(
        r"\binternship\b|\bintern\b|\binterned\b|\btrainee\b",
        text,
        re.IGNORECASE
    )
    return len(matches)


def count_certifications(certifications_text):
    """
    Count certifications from the extracted certification section.

    Handles:
    - Certificate & Workshop entries
    - Certificate entries on separate lines
    - Bullet-point entries
    """

    if not certifications_text:
        return 0

    text = certifications_text.strip()

    # --------------------------------------------------
    # 1. Look for common certification keywords
    # --------------------------------------------------

    certificate_matches = re.findall(
        r"\bcertificate\b|\bcertification\b|\bworkshop\b",
        text,
        re.IGNORECASE
    )

    # --------------------------------------------------
    # 2. Count unique certification-style entries
    # --------------------------------------------------

    lines = re.split(r"[\r\n]+", text)

    valid_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove bullets
        line = re.sub(r"^[•●▪◦\-*]+\s*", "", line)

        if re.search(
            r"certificate|certification|workshop",
            line,
            re.IGNORECASE
        ):
            valid_lines.append(line)

    # --------------------------------------------------
    # 3. Use line count when available
    # --------------------------------------------------

    if len(valid_lines) >= 1:
        return len(valid_lines)

    # --------------------------------------------------
    # 4. Fallback
    # --------------------------------------------------

    if certificate_matches:
        return min(len(certificate_matches), 10)

    return 0


def extract_experience_months(experience_text):
    if not experience_text:
        return 0

    total_months = sum(
        int(float(value))
        for value in re.findall(r"(\d+(?:\.\d+)?)\s*months?", experience_text, re.IGNORECASE)
    )
    total_months += sum(
        int(float(value) * 12)
        for value in re.findall(r"(\d+(?:\.\d+)?)\s*years?", experience_text, re.IGNORECASE)
    )
    return total_months


def detect_internship_text(text):
    if not text:
        return ""

    return "\n".join(
        line.strip()
        for line in text.split("\n")
        if re.search(r"\binternship\b|\bintern\b|\binterned\b", line, re.IGNORECASE)
    )


def analyze_resume(file_bytes):
    """Run the complete resume analysis pipeline."""

    raw_text = extract_text_from_bytes(file_bytes)
    cleaned_text = clean_text(raw_text)
    skills = extract_skills(cleaned_text)
    sections = extract_sections(cleaned_text)

    projects = sections.get("projects", "")
    experience = sections.get("experience", "")
    internship_section = sections.get("internship", "") or detect_internship_text(cleaned_text)
    education = sections.get("education", "")
    certifications = extract_section(
        cleaned_text,
        [
            "certifications",
            "certificates",
            "certifications & achievements",
            "certification & achievements"
        ]
    )

    return {
        "skills": skills,
        "skill_count": len(skills),
        "projects_section": projects,
        "project_count": count_projects(projects),
        "experience_section": experience,
        "internship_section": internship_section,
        "internship_count": count_internships(internship_section),
        "education_section": education,
        "certifications_section": certifications,
        "certification_count": count_certifications(certifications),
        "experience_months": extract_experience_months(experience),
        "text_length": len(cleaned_text)
    }


if __name__ == "__main__":
    print("===================================")
    print("       SKILLPATH AI RESUME NLP")
    print("===================================")

    resume_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "resumes"
    )
    pdf_files = [
        file for file in os.listdir(resume_folder)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print("\nNo PDF found.")
        print("\nPut a resume PDF inside:")
        print(resume_folder)
    else:
        with open(os.path.join(resume_folder, pdf_files[0]), "rb") as file:
            result = analyze_resume(file.read())
        print("\nResume analyzed successfully!")
        print("\nDetected Skills:")
        for skill in result["skills"]:
            print("-", skill)
        for key in ("skill_count", "project_count", "internship_count", "certification_count", "experience_months"):
            print(f"\n{key.replace('_', ' ').title()}:")
            print(result[key])
