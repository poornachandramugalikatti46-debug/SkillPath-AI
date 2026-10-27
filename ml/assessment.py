# --------------------------------------------------
# SkillPath AI - Student Assessment
# --------------------------------------------------

def calculate_assessment_score(
    technical_score,
    aptitude_score,
    problem_solving_score,
    communication_score,
    interview_confidence_score
):
    """
    Calculate an overall assessment score.

    All inputs should be between 0 and 100.
    """

    scores = [
        technical_score,
        aptitude_score,
        problem_solving_score,
        communication_score,
        interview_confidence_score
    ]

    # Validate scores
    for score in scores:

        if score < 0 or score > 100:

            raise ValueError(
                "All scores must be between 0 and 100."
            )

    # Weighted assessment score

    assessment_score = (
        technical_score * 0.30
        + aptitude_score * 0.15
        + problem_solving_score * 0.25
        + communication_score * 0.15
        + interview_confidence_score * 0.15
    )

    return round(
        assessment_score,
        2
    )


# --------------------------------------------------
# Convert assessment into ML features
# --------------------------------------------------

def create_assessment_features(
    technical_score,
    aptitude_score,
    problem_solving_score,
    communication_score,
    interview_confidence_score
):

    assessment_score = calculate_assessment_score(
        technical_score,
        aptitude_score,
        problem_solving_score,
        communication_score,
        interview_confidence_score
    )

    return {
        "technical_score": technical_score,
        "aptitude_score": aptitude_score,
        "problem_solving_score": problem_solving_score,
        "communication_score": communication_score,
        "interview_confidence_score":
            interview_confidence_score,
        "assessment_score":
            assessment_score
    }


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    print("\n===================================")
    print("       STUDENT ASSESSMENT")
    print("===================================")

    technical = 75
    aptitude = 70
    problem_solving = 80
    communication = 65
    interview_confidence = 70

    result = create_assessment_features(
        technical,
        aptitude,
        problem_solving,
        communication,
        interview_confidence
    )

    print("\nAssessment Results:\n")

    print(
        "Technical:",
        result["technical_score"]
    )

    print(
        "Aptitude:",
        result["aptitude_score"]
    )

    print(
        "Problem Solving:",
        result["problem_solving_score"]
    )

    print(
        "Communication:",
        result["communication_score"]
    )

    print(
        "Interview Confidence:",
        result["interview_confidence_score"]
    )

    print(
        "\nOverall Assessment Score:",
        result["assessment_score"]
    )