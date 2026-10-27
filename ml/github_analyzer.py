import requests
from datetime import datetime, timezone


# ==================================================
# GitHub API
# ==================================================

GITHUB_API = "https://api.github.com"


# ==================================================
# Extract username from GitHub URL
# ==================================================

def extract_username(github_url):
    """
    Extract GitHub username from a GitHub profile URL.
    """

    if not github_url:
        raise ValueError("GitHub URL is required.")

    github_url = github_url.strip().rstrip("/")

    # Remove query parameters
    github_url = github_url.split("?")[0]

    # Remove fragments
    github_url = github_url.split("#")[0]

    # Remove protocol
    github_url = github_url.replace("https://", "")
    github_url = github_url.replace("http://", "")

    # Remove GitHub domain
    github_url = github_url.replace("github.com/", "")

    # Remove accidental www
    github_url = github_url.replace("www.github.com/", "")

    username = github_url.split("/")[0].strip()

    if not username:
        raise ValueError("Invalid GitHub URL.")

    return username


# ==================================================
# GitHub API request helper
# ==================================================

def github_get(endpoint, params=None):

    url = f"{GITHUB_API}{endpoint}"

    response = requests.get(
        url,
        params=params,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "SkillPath-AI"
        },
        timeout=15
    )

    if response.status_code == 404:
        raise ValueError("GitHub user or resource not found.")

    if response.status_code == 403:
        raise ValueError(
            "GitHub API rate limit reached. "
            "Please try again later."
        )

    if response.status_code != 200:
        raise ValueError(
            f"GitHub API error: {response.status_code}"
        )

    return response.json()


# ==================================================
# Calculate recent activity
# ==================================================

def calculate_activity_score(
    repositories,
    language_count,
    project_count,
    star_count,
    fork_count
):
    """
    Calculate a simple 0-100 GitHub activity score.

    This is a SkillPath-AI project metric,
    not an official GitHub score.
    """

    score = (
        len(repositories) * 5
        + language_count * 5
        + project_count * 3
        + star_count * 2
        + fork_count * 2
    )

    # Add evidence for recently updated repositories
    recent_updates = 0

    now = datetime.now(timezone.utc)

    for repo in repositories:

        updated_at = repo.get("updated_at")

        if not updated_at:
            continue

        try:

            updated_date = datetime.fromisoformat(
                updated_at.replace("Z", "+00:00")
            )

            days_old = (
                now - updated_date
            ).days

            if days_old <= 180:
                recent_updates += 1

        except ValueError:
            continue

    score += recent_updates * 3

    return min(100, score)


# ==================================================
# Analyze repositories
# ==================================================

def analyze_repositories(repositories):

    repository_details = []

    languages = set()

    total_stars = 0
    total_forks = 0

    project_count = 0

    for repo in repositories:

        repo_name = repo.get(
            "name",
            ""
        )

        description = repo.get(
            "description"
        )

        language = repo.get(
            "language"
        )

        stars = repo.get(
            "stargazers_count",
            0
        )

        forks = repo.get(
            "forks_count",
            0
        )

        topics = repo.get(
            "topics",
            []
        )

        html_url = repo.get(
            "html_url"
        )

        updated_at = repo.get(
            "updated_at"
        )

        size = repo.get(
            "size",
            0
        )

        # ------------------------------------------
        # Language
        # ------------------------------------------

        if language:
            languages.add(language)

        # ------------------------------------------
        # Stars / forks
        # ------------------------------------------

        total_stars += stars
        total_forks += forks

        # ------------------------------------------
        # Project evidence
        # ------------------------------------------

        has_project_evidence = bool(
            description
            or size > 0
            or topics
        )

        if has_project_evidence:
            project_count += 1

        # ------------------------------------------
        # Repository details
        # ------------------------------------------

        repository_details.append({

            "name": repo_name,

            "description":
                description or "",

            "language":
                language or "",

            "stars":
                stars,

            "forks":
                forks,

            "topics":
                topics,

            "url":
                html_url,

            "updated_at":
                updated_at,

            "has_project_evidence":
                has_project_evidence
        })

    return {
        "repositories": repository_details,
        "languages": sorted(languages),
        "language_count": len(languages),
        "star_count": total_stars,
        "fork_count": total_forks,
        "project_count": project_count
    }


# ==================================================
# Create GitHub skill evidence
# ==================================================

def calculate_skill_evidence(
    repositories,
    languages
):
    """
    Estimate GitHub-based skill evidence.

    This does NOT claim actual proficiency.
    It only measures evidence found in
    public repositories.
    """

    evidence = {}

    # ------------------------------------------
    # Language evidence
    # ------------------------------------------

    for language in languages:

        if not language:
            continue

        skill = language.strip().lower()

        evidence[skill] = min(
            100,
            evidence.get(skill, 0) + 40
        )

    # ------------------------------------------
    # Repository-based evidence
    # ------------------------------------------

    technology_aliases = {

        "react": [
            "react",
            "reactjs"
        ],

        "node.js": [
            "node.js",
            "nodejs"
        ],

        "express.js": [
            "express.js",
            "expressjs"
        ],

        "python": [
            "python"
        ],

        "javascript": [
            "javascript",
            "javascript project",
            "javascript application"
        ],

        "typescript": [
            "typescript",
            "typescript project"
        ],

        "sql": [
            "sql",
            "mysql",
            "postgresql",
            "postgres"
        ],

        "mongodb": [
            "mongodb",
            "mongo db"
        ],

        "fastapi": [
            "fastapi"
        ],

        "django": [
            "django"
        ],

        "machine learning": [
            "machine learning",
            "machine-learning",
            "scikit-learn",
            "sklearn"
        ]
    }

    # ------------------------------------------
    # Check each repository
    # ------------------------------------------

    for repo in repositories:

        repo_name = str(
            repo.get("name", "")
        ).lower()

        description = str(
            repo.get("description", "")
        ).lower()

        topics = repo.get(
            "topics",
            []
        )

        topics_text = " ".join(
            str(topic).lower()
            for topic in topics
        )

        language = str(
            repo.get("language", "")
        ).lower()

        # Combine searchable repository evidence
        text = " ".join([
            repo_name,
            description,
            topics_text,
            language
        ])

        # --------------------------------------
        # Match skills safely
        # --------------------------------------

        for skill, aliases in technology_aliases.items():

            for alias in aliases:

                alias = alias.lower().strip()

                # Exact phrase/word-style matching
                words = text.replace(
                    "-", " "
                ).replace(
                    "_", " "
                ).split()

                normalized_text = " ".join(words)

                normalized_alias = alias.replace(
                    "-", " "
                ).replace(
                    "_", " "
                ).lower()

                if normalized_alias in normalized_text:

                    evidence[skill] = min(
                        100,
                        evidence.get(skill, 0) + 20
                    )

                    break

    # ------------------------------------------
    # Remove very weak / accidental evidence
    # ------------------------------------------

    evidence = {
        skill: score
        for skill, score in evidence.items()
        if score >= 20
    }

    return evidence


# ==================================================
# Main GitHub analyzer
# ==================================================

def analyze_github(github_url):

    username = extract_username(
        github_url
    )

    # ------------------------------------------
    # Get repositories
    # ------------------------------------------

    repositories = github_get(
        f"/users/{username}/repos",
        params={
            "per_page": 100,
            "sort": "updated"
        }
    )

    # ------------------------------------------
    # Analyze repositories
    # ------------------------------------------

    repository_analysis = analyze_repositories(
        repositories
    )

    languages = repository_analysis[
        "languages"
    ]

    language_count = repository_analysis[
        "language_count"
    ]

    star_count = repository_analysis[
        "star_count"
    ]

    fork_count = repository_analysis[
        "fork_count"
    ]

    project_count = repository_analysis[
        "project_count"
    ]

    # ------------------------------------------
    # Activity
    # ------------------------------------------

    activity_score = calculate_activity_score(
        repositories=repositories,
        language_count=language_count,
        project_count=project_count,
        star_count=star_count,
        fork_count=fork_count
    )

    # ------------------------------------------
    # Skill evidence
    # ------------------------------------------

    skill_evidence = calculate_skill_evidence(
        repositories=repository_analysis[
            "repositories"
        ],
        languages=languages
    )

    # ------------------------------------------
    # Final result
    # ------------------------------------------

    return {

        "github_url":
            github_url,

        "github_username":
            username,

        "github_repo_count":
            len(repositories),

        "github_language_count":
            language_count,

        "github_star_count":
            star_count,

        "github_fork_count":
            fork_count,

        "github_project_count":
            project_count,

        "github_activity_score":
            activity_score,

        "languages":
            languages,

        "repositories":
            repository_analysis[
                "repositories"
            ],

        "skill_evidence":
            skill_evidence
    }


# ==================================================
# Test
# ==================================================

if __name__ == "__main__":

    print("\n======================================")
    print("       SKILLPATH AI GITHUB ANALYZER")
    print("======================================")

    github_url = input(
        "\nEnter GitHub profile URL: "
    ).strip()

    try:

        result = analyze_github(
            github_url
        )

        print("\nGitHub Analysis")
        print("==============================")

        print(
            "Username:",
            result["github_username"]
        )

        print(
            "Repositories:",
            result["github_repo_count"]
        )

        print(
            "Languages:",
            result["github_language_count"]
        )

        print(
            "Stars:",
            result["github_star_count"]
        )

        print(
            "Forks:",
            result["github_fork_count"]
        )

        print(
            "Projects:",
            result["github_project_count"]
        )

        print(
            "Activity:",
            result["github_activity_score"]
        )

        print(
            "Languages:",
            ", ".join(
                result["languages"]
            )
        )

        print("\nGitHub Skill Evidence")
        print("==============================")

        for skill, score in sorted(
            result["skill_evidence"].items(),
            key=lambda item: item[1],
            reverse=True
        ):

            print(
                f"{skill}: {score}"
            )

        print("\nRepositories")
        print("==============================")

        for repo in result["repositories"]:

            print(
                f"- {repo['name']} "
                f"({repo['language'] or 'Unknown'})"
            )

    except Exception as error:

        print(
            "\nError:",
            error
        )