import { useEffect, useState } from "react";
import { analyzeStudent } from "../services/api";

function AnalyzeStudent({
  onAnalysisComplete,
  assessment,
}) {
  const [form, setForm] = useState({
    name: "",
    cgpa: "",
    target_role: "",
    location: "",
    github_url: "",

    technical_score: "",
    aptitude_score: "",
    problem_solving_score: "",
    communication_score: "",
    interview_confidence_score: "",
  });

  useEffect(() => {
    if (!assessment) {
      return;
    }

    setForm((previous) => ({
      ...previous,
      technical_score: assessment.technical_score ?? 0,
      aptitude_score: assessment.aptitude_score ?? 0,
      problem_solving_score:
        assessment.problem_solving_score ?? 0,
      communication_score:
        assessment.communication_score ?? 0,
      interview_confidence_score:
        assessment.interview_confidence_score ?? 0,
    }));
  }, [assessment]);

  const [resume, setResume] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [success, setSuccess] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  function handleResumeChange(event) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setError("Please upload a PDF resume.");
      setResume(null);
      return;
    }

    setError("");
    setResume(file);
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!resume) {
      setError("Please upload your resume PDF.");
      return;
    }

    if (!form.name.trim()) {
      setError("Please enter your name.");
      return;
    }

    if (!form.cgpa) {
      setError("Please enter your CGPA.");
      return;
    }

    if (!form.target_role.trim()) {
      setError("Please enter your target role.");
      return;
    }

    try {
      setLoading(true);

      const result = await analyzeStudent({
        ...form,
        file: resume,
      });

      localStorage.setItem(
        "skillpath_student_id",
        result.student_id
      );

      console.log("ML ANALYSIS RESULT:", result);

      setSuccess(
        "Analysis completed successfully! 🎉"
      );

      if (onAnalysisComplete) {
        onAnalysisComplete(result);
      }
    } catch (err) {
      console.error(err);

      const message =
        err.response?.data?.detail ||
        "Unable to analyze student. Please check the backend.";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-10 text-white">

      <div className="mx-auto max-w-5xl">

        {/* Header */}
        <div className="mb-8">

          <p className="text-sm font-medium text-cyan-400">
            SkillPath AI
          </p>

          <h1 className="mt-2 text-3xl font-bold">
            Analyze Your Career Readiness
          </h1>

          <p className="mt-2 text-slate-400">
            Enter your profile, upload your resume and provide
            your assessment scores.
          </p>

        </div>

        {/* Error */}
        {error && (
          <div className="mb-6 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
            {error}
          </div>
        )}

        {/* Success */}
        {success && (
          <div className="mb-6 rounded-xl border border-green-500/30 bg-green-500/10 p-4 text-sm text-green-400">
            {success}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="space-y-6"
        >

          {/* Profile */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              👤 Student Profile
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Basic information about you.
            </p>

            <div className="mt-6 grid gap-5 md:grid-cols-2">

              <Input
                label="Full Name"
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="Poornachandra"
              />

              <Input
                label="CGPA"
                name="cgpa"
                value={form.cgpa}
                onChange={handleChange}
                placeholder="7.7"
                type="number"
                step="0.1"
                min="0"
                max="10"
              />

              <Input
                label="Target Role"
                name="target_role"
                value={form.target_role}
                onChange={handleChange}
                placeholder="Backend Developer"
              />

              <Input
                label="Location"
                name="location"
                value={form.location}
                onChange={handleChange}
                placeholder="Bangalore"
              />

            </div>

          </section>

          {/* GitHub */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              💻 GitHub
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              We will analyze your public GitHub projects.
            </p>

            <div className="mt-5">

              <Input
                label="GitHub Profile URL"
                name="github_url"
                value={form.github_url}
                onChange={handleChange}
                placeholder="https://github.com/username"
              />

            </div>

          </section>

          {/* Resume */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              📄 Resume
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Upload your latest resume in PDF format.
            </p>

            <div className="mt-5">

              <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-700 bg-slate-950 p-8 transition hover:border-cyan-400">

                <span className="text-3xl">
                  📄
                </span>

                <span className="mt-3 text-sm font-medium">
                  Click to upload resume
                </span>

                <span className="mt-1 text-xs text-slate-500">
                  PDF files only
                </span>

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleResumeChange}
                  className="hidden"
                />

              </label>

              {resume && (
                <div className="mt-3 rounded-lg bg-green-500/10 p-3 text-sm text-green-400">
                  ✓ {resume.name}
                </div>
              )}

            </div>

          </section>

          {/* Assessment */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            {assessment ? (
              <div className="mb-6 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
                <p className="font-semibold text-emerald-400">
                  ✓ Assessment Completed
                </p>

                <p className="mt-1 text-sm text-slate-400">
                  Your assessment scores have been automatically
                  added to the ML analysis.
                </p>
              </div>
            ) : (
              <div className="mb-6 rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-4">
                <p className="font-semibold text-yellow-400">
                  Assessment Not Completed
                </p>

                <p className="mt-1 text-sm text-slate-400">
                  Complete the Assessment page first for more
                  complete ML analysis.
                </p>
              </div>
            )}

            <h2 className="text-xl font-semibold">
              📝 Assessment Scores
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Enter scores from 0 to 100.
            </p>

            <div className="mt-6 grid gap-5 md:grid-cols-2">

              <ScoreInput
                label="Technical Score"
                name="technical_score"
                value={form.technical_score}
                onChange={handleChange}
              />

              <ScoreInput
                label="Aptitude Score"
                name="aptitude_score"
                value={form.aptitude_score}
                onChange={handleChange}
              />

              <ScoreInput
                label="Problem Solving Score"
                name="problem_solving_score"
                value={form.problem_solving_score}
                onChange={handleChange}
              />

              <ScoreInput
                label="Communication Score"
                name="communication_score"
                value={form.communication_score}
                onChange={handleChange}
              />

              <ScoreInput
                label="Interview Confidence"
                name="interview_confidence_score"
                value={form.interview_confidence_score}
                onChange={handleChange}
              />

            </div>

          </section>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-cyan-400 px-6 py-4 font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
          >

            {loading
              ? "Analyzing with ML... ⏳"
              : "Analyze My Career Readiness 🚀"}

          </button>

        </form>

      </div>

    </div>
  );
}


/* -------------------------------- */
/* Text Input */
/* -------------------------------- */

function Input({
  label,
  name,
  value,
  onChange,
  placeholder,
  type = "text",
  ...props
}) {
  return (
    <div>

      <label className="mb-2 block text-sm font-medium">
        {label}
      </label>

      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400"
        {...props}
      />

    </div>
  );
}


/* -------------------------------- */
/* Score Input */
/* -------------------------------- */

function ScoreInput({
  label,
  name,
  value,
  onChange,
}) {
  return (
    <div>

      <label className="mb-2 block text-sm font-medium">
        {label}
      </label>

      <input
        type="number"
        name={name}
        value={value}
        onChange={onChange}
        placeholder="0 - 100"
        min="0"
        max="100"
        className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400"
      />

    </div>
  );
}

export default AnalyzeStudent;