import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

QUESTIONS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "assessment_questions.json"
)

VALID_DIFFICULTIES = {"easy", "medium", "hard"}

ROLE_ALIASES = {
    "python developer": "python_developer",
    "backend developer": "backend_developer",
    "data analyst": "data_analyst",
    "ml engineer": "ml_engineer",
    "machine learning engineer": "ml_engineer",
    "full stack developer": "full_stack_developer",
    "fullstack developer": "full_stack_developer",
    "full stack engineer": "full_stack_developer",
    "full_stack_developer": "full_stack_developer",
}


def normalize_role(role):
    """Convert a career role into a consistent identifier."""
    if not role:
        return None

    role = str(role).strip().lower()

    if role in ROLE_ALIASES:
        return ROLE_ALIASES[role]

    return role.replace(" ", "_").replace("-", "_")


def load_questions(role=None, difficulty=None):
    """
    Load questions and optionally filter by career role
    and difficulty.

    Questions without role metadata remain shared questions,
    so your existing question bank stays compatible.
    """
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list):
        raise ValueError("The question bank must be a JSON list.")

    selected_role = normalize_role(role)

    selected_difficulty = None
    if difficulty:
        selected_difficulty = str(difficulty).strip().lower()

        if selected_difficulty not in VALID_DIFFICULTIES:
            raise ValueError(
                "Difficulty must be easy, medium, or hard."
            )

    filtered = []

    for question in questions:
        question_difficulty = str(
            question.get("difficulty", "easy")
        ).lower()

        if (
            selected_difficulty
            and question_difficulty != selected_difficulty
        ):
            continue

        question_roles = question.get("roles")

        if question_roles is None:
            legacy_role = question.get("role")

            if legacy_role:
                question_roles = [legacy_role]
            else:
                question_roles = None
        elif isinstance(question_roles, str):
            question_roles = [question_roles]

        if selected_role and question_roles:
            normalized_roles = {
                normalize_role(item)
                for item in question_roles
            }

            if selected_role not in normalized_roles:
                continue

        filtered.append(question)

    return filtered


def calculate_category_score(questions, answers, category):
    """Calculate the percentage score for one category."""
    category_questions = [
        question
        for question in questions
        if question.get("category") == category
    ]

    if not category_questions:
        return 0.0

    correct = 0

    for question in category_questions:
        question_id = str(question["id"])
        user_answer = answers.get(question_id)

        if (
            user_answer is not None
            and str(user_answer).strip().lower()
            == str(question["answer"]).strip().lower()
        ):
            correct += 1

    return round(
        (correct / len(category_questions)) * 100,
        2
    )


def calculate_assessment(
    answers,
    communication_score=0,
    interview_confidence_score=0,
    role=None,
    question_ids=None,
):
    """
    Score the submitted answers.

    Correct answers and explanations are returned only after
    submission, never from the public questions endpoint.
    """
    if not isinstance(answers, dict):
        raise ValueError("Answers must be a dictionary.")

    questions = load_questions(role=role)

    if question_ids is not None:
        if not isinstance(question_ids, list):
            raise ValueError("question_ids must be a list.")

        requested_ids = {str(item) for item in question_ids}
        questions = [
            question
            for question in questions
            if str(question["id"]) in requested_ids
        ]

    if not questions:
        raise ValueError("No valid assessment questions found.")

    valid_ids = {str(question["id"]) for question in questions}
    clean_answers = {
        str(key): value
        for key, value in answers.items()
        if str(key) in valid_ids
    }

    def safe_score(value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = 0.0

        return round(max(0.0, min(100.0, value)), 2)

    technical_score = calculate_category_score(
        questions, clean_answers, "technical"
    )
    aptitude_score = calculate_category_score(
        questions, clean_answers, "aptitude"
    )
    problem_solving_score = calculate_category_score(
        questions, clean_answers, "problem_solving"
    )

    correct_answers = 0
    review = []

    for question in questions:
        question_id = str(question["id"])
        selected_answer = clean_answers.get(question_id)
        correct_answer = question["answer"]

        is_correct = (
            selected_answer is not None
            and str(selected_answer).strip().lower()
            == str(correct_answer).strip().lower()
        )

        if is_correct:
            correct_answers += 1

        review.append({
            "id": question["id"],
            "question": question["question"],
            "category": question.get("category", "technical"),
            "difficulty": question.get("difficulty", "easy"),
            "selected_answer": selected_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.get(
                "explanation",
                "Review this topic and practise similar questions."
            ),
        })

    total_questions = len(questions)
    answered_questions = len(clean_answers)
    accuracy = round(
        (correct_answers / total_questions) * 100,
        2
    )

    return {
        "technical_score": technical_score,
        "aptitude_score": aptitude_score,
        "problem_solving_score": problem_solving_score,
        "communication_score": safe_score(communication_score),
        "interview_confidence_score": safe_score(
            interview_confidence_score
        ),
        "role": normalize_role(role),
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "correct_answers": correct_answers,
        "incorrect_answers": answered_questions - correct_answers,
        "accuracy": accuracy,
        "category_scores": {
            "technical": technical_score,
            "aptitude": aptitude_score,
            "problem_solving": problem_solving_score,
        },
        "review": review,
    }
