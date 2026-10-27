import { useCallback, useEffect, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../services/api";

const EXAM_DURATION = 20 * 60;

const CAREER_ROLES = [
  "Python Developer",
  "Backend Developer",
  "Full Stack Developer",
  "Data Analyst",
  "ML Engineer",
];

const DIFFICULTIES = ["easy", "medium", "hard"];

export default function Assessment({ onAssessmentComplete }) {
  const [role, setRole] = useState("Python Developer");
  const [difficulty, setDifficulty] = useState("easy");

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [current, setCurrent] = useState(0);

  const [timeLeft, setTimeLeft] = useState(EXAM_DURATION);
  const [communicationScore, setCommunicationScore] = useState(50);
  const [confidenceScore, setConfidenceScore] = useState(50);

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const loadQuestions = useCallback(
    async (selectedRole = role, selectedDifficulty = difficulty) => {
      setLoading(true);
      setError("");
      setResult(null);
      setSubmitted(false);
      setAnswers({});
      setCurrent(0);
      setTimeLeft(EXAM_DURATION);

      try {
        const response = await axios.get(
          `${API_BASE_URL}/api/assessment/questions`,
          {
            params: {
              role: selectedRole,
              difficulty: selectedDifficulty,
            },
          }
        );

        const loadedQuestions = response.data?.questions || [];

        if (loadedQuestions.length === 0) {
          setQuestions([]);
          setError(
            "No questions are available for this selection. " +
              "Check the question bank."
          );
          return;
        }

        setQuestions(loadedQuestions);
      } catch (err) {
        setQuestions([]);
        setError(
          err.response?.data?.detail ||
            "Could not load questions. Check that FastAPI is running."
        );
      } finally {
        setLoading(false);
      }
    },
    [role, difficulty]
  );

  useEffect(() => {
    loadQuestions("Python Developer", "easy");
  }, []);

  const submitAssessment = useCallback(
    async (automatic = false) => {
      if (submitting || submitted || questions.length === 0) {
        return;
      }

      setSubmitting(true);
      setError("");

      try {
        const response = await axios.post(
          `${API_BASE_URL}/api/assessment/submit`,
          {
            role,
            difficulty,
            answers,
            question_ids: questions.map((question) => question.id),
            communication_score: communicationScore,
            interview_confidence_score: confidenceScore,
            automatic_submission: automatic,
          }
        );

        setResult(response.data.assessment);
        setSubmitted(true);

        if (onAssessmentComplete) {
          onAssessmentComplete(response.data.assessment);
        }
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Assessment submission failed. Please try again."
        );
      } finally {
        setSubmitting(false);
      }
    },
    [
      answers,
      communicationScore,
      confidenceScore,
      difficulty,
      onAssessmentComplete,
      questions,
      role,
      submitted,
      submitting,
    ]
  );

  useEffect(() => {
    if (loading || submitted || questions.length === 0) {
      return undefined;
    }

    const timer = setInterval(() => {
      setTimeLeft((previous) => Math.max(0, previous - 1));
    }, 1000);

    return () => clearInterval(timer);
  }, [loading, submitted, questions.length]);

  useEffect(() => {
    if (
      !loading &&
      !submitted &&
      timeLeft === 0 &&
      questions.length > 0
    ) {
      submitAssessment(true);
    }
  }, [
    timeLeft,
    loading,
    submitted,
    questions.length,
    submitAssessment,
  ]);

  const question = questions[current];

  const answeredCount = questions.filter(
    (item) => answers[String(item.id)] !== undefined
  ).length;

  const progress =
    questions.length > 0
      ? (answeredCount / questions.length) * 100
      : 0;

  const formattedTime = `${String(
    Math.floor(timeLeft / 60)
  ).padStart(2, "0")}:${String(timeLeft % 60).padStart(
    2,
    "0"
  )}`;

  function chooseRole(nextRole) {
    setRole(nextRole);
    loadQuestions(nextRole, difficulty);
  }

  function chooseDifficulty(nextDifficulty) {
    setDifficulty(nextDifficulty);
    loadQuestions(role, nextDifficulty);
  }

  function chooseAnswer(questionId, answer) {
    setAnswers((previous) => ({
      ...previous,
      [String(questionId)]: answer,
    }));
  }

  function formatCategory(category) {
    return String(category || "")
      .replaceAll("_", " ")
      .replace(/\b\w/g, (character) => character.toUpperCase());
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-950 p-8 text-white">
        <div className="mx-auto max-w-4xl rounded-2xl border border-slate-800 bg-slate-900 p-8">
          <p className="animate-pulse text-lg">Loading your assessment...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-8 text-slate-100 sm:px-8">
      <div className="mx-auto max-w-5xl space-y-6">
        <header>
          <p className="text-sm font-semibold uppercase tracking-widest text-cyan-400">
            SkillPath-AI
          </p>

          <h1 className="mt-2 text-3xl font-bold">Career Readiness Assessment</h1>

          <p className="mt-2 text-slate-400">
            Test your knowledge and identify areas to improve.
          </p>
        </header>

        {error && (
          <div
            role="alert"
            className="rounded-xl border border-red-800 bg-red-950/50 p-4 text-red-200"
          >
            {error}
          </div>
        )}

        {!submitted && (
          <>
            <section className="grid gap-4 rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:grid-cols-2 sm:p-6">
              <div>
                <label className="mb-2 block text-sm text-slate-300">
                  Career role
                </label>
                <select
                  value={role}
                  onChange={(event) => chooseRole(event.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-white focus:border-cyan-400 focus:outline-none"
                >
                  {CAREER_ROLES.map((careerRole) => (
                    <option key={careerRole} value={careerRole}>
                      {careerRole}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm text-slate-300">
                  Difficulty
                </label>
                <select
                  value={difficulty}
                  onChange={(event) => chooseDifficulty(event.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-white focus:border-cyan-400 focus:outline-none"
                >
                  {DIFFICULTIES.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </select>
              </div>
            </section>

            {questions.length > 0 && (
              <>
                <section className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                  <StatCard label="Questions" value={questions.length} />
                  <StatCard
                    label="Answered"
                    value={`${answeredCount}/${questions.length}`}
                  />
                  <StatCard
                    label="Progress"
                    value={`${Math.round(progress)}%`}
                  />
                  <StatCard
                    label="Time left"
                    value={formattedTime}
                    warning={timeLeft < 60}
                  />
                </section>

                <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-cyan-400 transition-all"
                    style={{ width: `${progress}%` }}
                  />
                </div>

                <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:p-8">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <span className="text-sm text-slate-400">
                      Question {current + 1} of {questions.length}
                    </span>

                    <div className="flex gap-2">
                      <span className="rounded-full bg-slate-800 px-3 py-1 text-xs capitalize">
                        {formatCategory(question?.category)}
                      </span>

                      <span className="rounded-full bg-cyan-950 px-3 py-1 text-xs capitalize text-cyan-300">
                        {question?.difficulty || "easy"}
                      </span>
                    </div>
                  </div>

                  <h2 className="mt-6 text-xl font-semibold leading-relaxed sm:text-2xl">
                    {question?.question}
                  </h2>

                  <div className="mt-6 space-y-3">
                    {question?.options?.map((option, index) => {
                      const selected = answers[String(question.id)] === option;

                      return (
                        <button
                          key={`${question.id}-${option}`}
                          type="button"
                          onClick={() => chooseAnswer(question.id, option)}
                          className={`flex w-full items-start gap-3 rounded-xl border p-4 text-left transition ${
                            selected
                              ? "border-cyan-400 bg-cyan-950/50"
                              : "border-slate-700 bg-slate-950 hover:border-slate-500"
                          }`}
                        >
                          <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-slate-800 text-sm">
                            {String.fromCharCode(65 + index)}
                          </span>

                          <span>{option}</span>
                        </button>
                      );
                    })}
                  </div>

                  <div className="mt-8 flex flex-wrap justify-between gap-3">
                    <button
                      type="button"
                      disabled={current === 0}
                      onClick={() => setCurrent((previous) => previous - 1)}
                      className="rounded-lg border border-slate-700 px-5 py-3 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      Previous
                    </button>

                    {current < questions.length - 1 ? (
                      <button
                        type="button"
                        onClick={() => setCurrent((previous) => previous + 1)}
                        className="rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-300"
                      >
                        Next question
                      </button>
                    ) : (
                      <button
                        type="button"
                        disabled={submitting}
                        onClick={() => submitAssessment(false)}
                        className="rounded-lg bg-emerald-400 px-5 py-3 font-semibold text-slate-950 disabled:opacity-50"
                      >
                        {submitting ? "Submitting..." : "Submit assessment"}
                      </button>
                    )}
                  </div>
                </section>

                <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
                  <h3 className="font-semibold">Jump to question</h3>

                  <div className="mt-4 flex flex-wrap gap-2">
                    {questions.map((item, index) => {
                      const answered = answers[String(item.id)] !== undefined;

                      return (
                        <button
                          key={item.id}
                          type="button"
                          onClick={() => setCurrent(index)}
                          aria-label={`Go to question ${index + 1}`}
                          className={`h-10 w-10 rounded-lg border text-sm ${
                            current === index
                              ? "border-cyan-400 bg-cyan-400 font-bold text-slate-950"
                              : answered
                                ? "border-emerald-500 bg-emerald-950 text-emerald-300"
                                : "border-slate-700 bg-slate-950"
                          }`}
                        >
                          {index + 1}
                        </button>
                      );
                    })}
                  </div>

                  <p className="mt-3 text-xs text-slate-400">
                    Cyan: current question - Green: answered - Dark: unanswered
                  </p>
                </section>

                <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:p-7">
                  <h3 className="text-lg font-semibold">Self-assessment</h3>

                  <p className="mt-1 text-sm text-slate-400">
                    Rate yourself honestly. These ratings are not automatically
                    verified by the quiz.
                  </p>

                  <ScoreSlider
                    label="Communication"
                    value={communicationScore}
                    onChange={setCommunicationScore}
                  />

                  <ScoreSlider
                    label="Interview confidence"
                    value={confidenceScore}
                    onChange={setConfidenceScore}
                  />
                </section>

                <button
                  type="button"
                  disabled={submitting}
                  onClick={() => submitAssessment(false)}
                  className="w-full rounded-xl bg-emerald-400 px-5 py-4 font-bold text-slate-950 hover:bg-emerald-300 disabled:opacity-50"
                >
                  {submitting
                    ? "Submitting assessment..."
                    : `Submit assessment (${answeredCount}/${questions.length} answered)`}
                </button>
              </>
            )}
          </>
        )}

        {submitted && result && (
          <section className="space-y-6">
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 sm:p-8">
              <p className="text-sm text-cyan-400">Assessment completed</p>

              <h2 className="mt-2 text-2xl font-bold">Your results</h2>

              <p className="mt-1 text-slate-400">
                Role: {role} - Difficulty: {difficulty}
              </p>

              <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
                <StatCard label="Accuracy" value={`${result.accuracy ?? 0}%`} />
                <StatCard label="Correct" value={result.correct_answers ?? 0} />
                <StatCard
                  label="Answered"
                  value={`${result.answered_questions ?? 0}/${result.total_questions ?? questions.length}`}
                />
                <StatCard
                  label="Technical"
                  value={`${result.technical_score ?? 0}%`}
                />
                <StatCard
                  label="Aptitude"
                  value={`${result.aptitude_score ?? 0}%`}
                />
                <StatCard
                  label="Problem solving"
                  value={`${result.problem_solving_score ?? 0}%`}
                />
                <StatCard
                  label="Communication"
                  value={`${result.communication_score ?? 0}%`}
                />
                <StatCard
                  label="Interview confidence"
                  value={`${result.interview_confidence_score ?? 0}%`}
                />
              </div>

              <button
                type="button"
                onClick={() => loadQuestions(role, difficulty)}
                className="mt-6 rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950"
              >
                Retake assessment
              </button>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:p-7">
              <h3 className="text-xl font-bold">Answer review</h3>

              <div className="mt-5 space-y-4">
                {(result.review || []).map((item) => (
                  <article
                    key={item.id}
                    className="rounded-xl border border-slate-800 bg-slate-950 p-4"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <span className="text-sm text-slate-400">
                        Question {item.id} - {formatCategory(item.category)}
                      </span>

                      <span
                        className={
                          item.is_correct
                            ? "text-sm font-semibold text-emerald-400"
                            : "text-sm font-semibold text-red-400"
                        }
                      >
                        {item.is_correct ? "Correct" : "Incorrect"}
                      </span>
                    </div>

                    <p className="mt-3 font-semibold">{item.question}</p>

                    <p className="mt-2 text-sm text-slate-400">
                      Your answer: {item.selected_answer ?? "Not answered"}
                    </p>

                    <p className="mt-1 text-sm text-emerald-300">
                      Correct answer: {item.correct_answer}
                    </p>

                    <p className="mt-3 text-sm leading-relaxed text-slate-300">
                      {item.explanation}
                    </p>
                  </article>
                ))}
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}

function StatCard({ label, value, warning = false }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
      <p className="text-xs text-slate-400">{label}</p>
      <p
        className={`mt-2 text-xl font-bold ${
          warning ? "text-red-400" : "text-white"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function ScoreSlider({ label, value, onChange }) {
  return (
    <div className="mt-6">
      <div className="mb-2 flex items-center justify-between gap-3">
        <label className="text-sm text-slate-300">{label}</label>
        <span className="font-semibold text-cyan-300">{value}/100</span>
      </div>

      <input
        type="range"
        min="0"
        max="100"
        step="5"
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
        className="w-full accent-cyan-400"
      />
    </div>
  );
}
