import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Load learning resources
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RESOURCES_FILE = os.path.join(
    BASE_DIR,
    "data",
    "resources.json"
)


def load_resources():
    """Load learning resources from resources.json."""

    with open(
        RESOURCES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------------------------
# 2. Prepare resource documents
# --------------------------------------------------

def create_resource_documents(resources):
    """
    Convert each learning resource into searchable text.
    """

    documents = []

    for resource in resources:

        title = resource.get(
            "title",
            ""
        )

        skills = resource.get(
            "skills",
            []
        )

        description = resource.get(
            "description",
            ""
        )

        text = (
            str(title)
            + " "
            + " ".join(
                str(skill)
                for skill in skills
            )
            + " "
            + str(description)
        )

        documents.append(text)

    return documents


# --------------------------------------------------
# 3. Create priority from skill gap
# --------------------------------------------------

def calculate_priority(gap):
    """
    Convert skill gap into recommendation priority.
    """

    if gap >= 40:
        return "High"

    if gap >= 20:
        return "Medium"

    return "Low"


# --------------------------------------------------
# 4. Generate recommendations
# --------------------------------------------------

def generate_recommendations(
    skill_gaps,
    top_n=5
):
    """
    Generate personalized learning recommendations
    from the student's actual skill gaps.
    """

    resources = load_resources()

    if not skill_gaps:
        return []

    # ----------------------------------------------
    # Convert skill gaps into clean query
    # ----------------------------------------------

    gap_skills = []

    for gap in skill_gaps:

        skill = gap.get(
            "skill",
            ""
        )

        if skill:
            gap_skills.append(
                str(skill)
            )

    if not gap_skills:
        return []

    # ----------------------------------------------
    # Create resource documents
    # ----------------------------------------------

    resource_documents = (
        create_resource_documents(
            resources
        )
    )

    # ----------------------------------------------
    # TF-IDF
    # ----------------------------------------------

    vectorizer = TfidfVectorizer()

    resource_vectors = (
        vectorizer.fit_transform(
            resource_documents
        )
    )

    # ----------------------------------------------
    # Create student query
    # ----------------------------------------------

    student_query = " ".join(
        gap_skills
    )

    student_vector = (
        vectorizer.transform(
            [student_query]
        )
    )

    # ----------------------------------------------
    # Cosine similarity
    # ----------------------------------------------

    similarity_scores = (
        cosine_similarity(
            student_vector,
            resource_vectors
        )[0]
    )

    # ----------------------------------------------
    # Create recommendations
    # ----------------------------------------------

    recommendations = []

    for index, score in enumerate(
        similarity_scores
    ):

        resource = resources[index]

        recommendations.append({

            "title": resource.get(
                "title",
                ""
            ),

            "type": resource.get(
                "type",
                ""
            ),

            "skills": resource.get(
                "skills",
                []
            ),

            "difficulty": resource.get(
                "difficulty",
                ""
            ),

            "similarity_score": round(
                float(score),
                4
            )
        })

    # ----------------------------------------------
    # Sort by similarity
    # ----------------------------------------------

    recommendations.sort(
        key=lambda item:
            item["similarity_score"],
        reverse=True
    )

    # ----------------------------------------------
    # Return top recommendations
    # ----------------------------------------------

    return recommendations[:top_n]


# --------------------------------------------------
# 5. Generate skill-wise recommendations
# --------------------------------------------------

def generate_skill_recommendations(
    skill_gaps,
    resources_per_skill=2
):
    """
    Generate recommendations separately
    for each skill gap.
    """

    resources = load_resources()

    if not skill_gaps:
        return []

    resource_documents = (
        create_resource_documents(
            resources
        )
    )

    vectorizer = TfidfVectorizer()

    resource_vectors = (
        vectorizer.fit_transform(
            resource_documents
        )
    )

    results = []

    # ----------------------------------------------
    # Process each skill gap
    # ----------------------------------------------

    for gap in skill_gaps:

        skill = gap.get(
            "skill",
            ""
        )

        required_score = gap.get(
            "required_score",
            0
        )

        student_score = gap.get(
            "student_score",
            0
        )

        gap_value = gap.get(
            "gap",
            0
        )

        if not skill:
            continue

        # ------------------------------------------
        # Create query for this skill
        # ------------------------------------------

        skill_query = str(skill)

        skill_vector = (
            vectorizer.transform(
                [skill_query]
            )
        )

        similarity_scores = (
            cosine_similarity(
                skill_vector,
                resource_vectors
            )[0]
        )

        # ------------------------------------------
        # Sort resource indexes
        # ------------------------------------------

        ranked_indexes = sorted(
            range(
                len(similarity_scores)
            ),
            key=lambda index:
                similarity_scores[index],
            reverse=True
        )

        selected_resources = []

        # ------------------------------------------
        # Select useful resources
        # ------------------------------------------

        for index in ranked_indexes:

            score = float(
                similarity_scores[index]
            )

            # Ignore completely unrelated resources
            if score <= 0:
                continue

            resource = resources[index]

            selected_resources.append({

                "title": resource.get(
                    "title",
                    ""
                ),

                "type": resource.get(
                    "type",
                    ""
                ),

                "skills": resource.get(
                    "skills",
                    []
                ),

                "difficulty": resource.get(
                    "difficulty",
                    ""
                ),

                "similarity_score": round(
                    score,
                    4
                )
            })

            if len(
                selected_resources
            ) >= resources_per_skill:

                break

        # ------------------------------------------
        # Add skill recommendation
        # ------------------------------------------

        results.append({

            "skill": skill,

            "required_score": required_score,

            "student_score": student_score,

            "gap": gap_value,

            "priority": calculate_priority(
                gap_value
            ),

            "resources": selected_resources
        })

    # ----------------------------------------------
    # Highest gap first
    # ----------------------------------------------

    results.sort(
        key=lambda item:
            item["gap"],
        reverse=True
    )

    return results


# --------------------------------------------------
# 6. Test
# --------------------------------------------------

if __name__ == "__main__":

    test_skill_gaps = [

        {
            "skill": "SQL",
            "required_score": 80,
            "student_score": 20,
            "gap": 60
        },

        {
            "skill": "Git",
            "required_score": 60,
            "student_score": 20,
            "gap": 40
        },

        {
            "skill": "REST API",
            "required_score": 80,
            "student_score": 60,
            "gap": 20
        },

        {
            "skill": "Python",
            "required_score": 70,
            "student_score": 55,
            "gap": 15
        }
    ]

    recommendations = (
        generate_skill_recommendations(
            test_skill_gaps
        )
    )

    print("\n========================================")
    print("       SKILLPATH AI RECOMMENDATIONS")
    print("========================================")

    for item in recommendations:

        print(
            f"\nSkill: {item['skill']}"
        )

        print(
            f"Required: "
            f"{item['required_score']}"
        )

        print(
            f"Student: "
            f"{item['student_score']}"
        )

        print(
            f"Gap: "
            f"{item['gap']}"
        )

        print(
            f"Priority: "
            f"{item['priority']}"
        )

        print("\nResources:")

        for resource in item[
            "resources"
        ]:

            print(
                f"  - {resource['title']}"
            )

            print(
                f"    Type: "
                f"{resource['type']}"
            )

            print(
                f"    Difficulty: "
                f"{resource['difficulty']}"
            )

            print(
                f"    Similarity: "
                f"{resource['similarity_score']}"
            )