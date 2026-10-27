import { useEffect, useState } from "react";
import { API_BASE_URL } from "../services/api";

function normalizeGithubData(data) {
  if (!data) {
    return null;
  }

  return {
    ...data,
    github_url: data.github_url || "",
    github_repo_count:
      data.github_repo_count ?? data.repository_count ?? 0,
    github_language_count:
      data.github_language_count ?? data.language_count ?? 0,
    github_star_count:
      data.github_star_count ?? data.stars ?? 0,
    github_fork_count:
      data.github_fork_count ?? data.forks ?? 0,
    github_project_count:
      data.github_project_count ??
      data.project_count ??
      data.repository_count ??
      0,
    github_activity_score:
      data.github_activity_score ?? data.activity_score ?? 0,
    languages: data.languages || [],
    skill_evidence: data.skill_evidence || {},
  };
}

export default function GitHub({ analysis }) {
  const [github, setGithub] = useState(
    normalizeGithubData(analysis?.github_analysis)
  );

  const [loading, setLoading] = useState(!analysis);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadGitHubData = async () => {
      try {
        // If analysis is already available, use it
        if (analysis?.github_analysis) {
          setGithub(normalizeGithubData(analysis.github_analysis));
          setLoading(false);
          return;
        }

        // Get saved student ID
        const studentId = localStorage.getItem(
          "skillpath_student_id"
        );

        if (!studentId) {
          setLoading(false);
          return;
        }

        // Fetch saved student dashboard
        const response = await fetch(
          `${API_BASE_URL}/api/student/${studentId}/dashboard`
        );

        if (!response.ok) {
          throw new Error("Failed to load GitHub analysis");
        }

        const data = await response.json();

        console.log("GitHub dashboard data:", data);

        setGithub(
          normalizeGithubData(
            data?.github_analysis || data?.github
          )
        );
      } catch (err) {
        console.error("GitHub page error:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadGitHubData();
  }, [analysis]);

  // =========================
  // LOADING
  // =========================

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white p-6 md:p-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-cyan-400 text-xs font-bold tracking-[0.2em] uppercase">
            SkillPath AI
          </p>

          <h1 className="text-3xl md:text-4xl font-bold mt-2">
            GitHub Analysis
          </h1>

          <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-900/70 p-10 text-center">
            <div className="w-10 h-10 mx-auto rounded-full border-4 border-slate-700 border-t-cyan-400 animate-spin" />

            <p className="text-slate-400 mt-5">
              Loading GitHub analysis...
            </p>
          </div>
        </div>
      </div>
    );
  }

  // =========================
  // ERROR
  // =========================

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 text-white p-6 md:p-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-cyan-400 text-xs font-bold tracking-[0.2em] uppercase">
            SkillPath AI
          </p>

          <h1 className="text-3xl font-bold mt-2">
            GitHub Analysis
          </h1>

          <div className="mt-8 rounded-2xl border border-red-500/20 bg-red-500/10 p-6">
            <h2 className="text-lg font-semibold text-red-300">
              Unable to load GitHub analysis
            </h2>

            <p className="text-slate-400 mt-2">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  // =========================
  // NO DATA
  // =========================

  if (!github) {
    return (
      <div className="min-h-screen bg-slate-950 text-white p-6 md:p-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-cyan-400 text-xs font-bold tracking-[0.2em] uppercase">
            SkillPath AI
          </p>

          <h1 className="text-3xl md:text-4xl font-bold mt-2">
            GitHub Analysis
          </h1>

          <p className="text-slate-400 mt-2">
            Analyze your coding activity, projects and technical evidence.
          </p>

          <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-900/70 p-12 text-center">
            <div className="w-20 h-20 mx-auto rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-4xl">
              🐙
            </div>

            <h2 className="text-2xl font-bold mt-6">
              No GitHub Analysis Yet
            </h2>

            <p className="text-slate-400 max-w-md mx-auto mt-3">
              Complete a student analysis with your GitHub profile
              to generate your GitHub metrics and skill evidence.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const activity = Math.min(
    100,
    Math.max(0, Number(github.github_activity_score) || 0)
  );

  const skillEvidence = github.skill_evidence || {};

  const sortedSkills = Object.entries(skillEvidence)
    .sort(([, a], [, b]) => Number(b) - Number(a))
    .slice(0, 10);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-5 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* ================= HEADER ================= */}

        <div className="mb-8">
          <div className="flex items-center gap-2 text-cyan-400 text-xs font-bold tracking-[0.2em] uppercase">
            <span className="w-2 h-2 rounded-full bg-cyan-400" />
            SkillPath AI
          </div>

          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mt-2">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold">
                GitHub Analysis
              </h1>

              <p className="text-slate-400 mt-2">
                Your coding activity, projects and technical skill evidence.
              </p>
            </div>

            {github.github_url && (
              <a
                href={github.github_url}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-cyan-400 text-slate-950 font-semibold hover:bg-cyan-300 transition"
              >
                View GitHub
                <span>↗</span>
              </a>
            )}
          </div>
        </div>

        {/* ================= PROFILE ================= */}

        <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-900/60 p-6 md:p-7 mb-6">
          <div className="absolute -top-20 -right-20 w-60 h-60 bg-cyan-500/10 blur-3xl rounded-full" />

          <div className="relative flex flex-col md:flex-row md:items-center gap-5">
            <div className="w-16 h-16 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-3xl">
              🐙
            </div>

            <div className="min-w-0 flex-1">
              <p className="text-slate-400 text-sm">
                GitHub Developer Profile
              </p>

              <h2 className="text-xl md:text-2xl font-bold mt-1">
                Coding Activity Overview
              </h2>

              {github.github_url && (
                <p className="text-slate-500 text-sm mt-2 truncate">
                  {github.github_url}
                </p>
              )}
            </div>

            <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-400/10 border border-emerald-400/20">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />

              <span className="text-emerald-300 text-sm font-medium">
                Profile Connected
              </span>
            </div>
          </div>
        </div>

        {/* ================= METRICS ================= */}

        <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          <MetricCard
            icon="📦"
            title="Repositories"
            value={github.github_repo_count}
          />

          <MetricCard
            icon="💻"
            title="Languages"
            value={github.github_language_count}
          />

          <MetricCard
            icon="⭐"
            title="Stars"
            value={github.github_star_count}
          />

          <MetricCard
            icon="🍴"
            title="Forks"
            value={github.github_fork_count}
          />

          <MetricCard
            icon="🚀"
            title="Projects"
            value={github.github_project_count}
          />

          <MetricCard
            icon="⚡"
            title="Activity"
            value={activity}
            suffix="/100"
          />
        </div>

        {/* ================= ACTIVITY + LANGUAGES ================= */}

        <div className="grid lg:grid-cols-3 gap-6 mt-6">
          <div className="lg:col-span-2 rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-cyan-400 text-xs font-semibold uppercase tracking-wider">
                  Developer Activity
                </p>

                <h2 className="text-xl font-bold mt-1">
                  GitHub Activity Score
                </h2>

                <p className="text-slate-400 text-sm mt-2">
                  Overall activity calculated from your GitHub profile.
                </p>
              </div>

              <div className="text-right">
                <p className="text-3xl font-bold text-cyan-400">{activity}</p>
                <p className="text-xs text-slate-500">/ 100</p>
              </div>
            </div>

            <div className="mt-8">
              <div className="h-4 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
                  style={{
                    width: `${activity}%`,
                  }}
                />
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
            <p className="text-cyan-400 text-xs font-semibold uppercase tracking-wider">
              Tech Stack
            </p>

            <h2 className="text-xl font-bold mt-1">Languages</h2>

            <div className="flex flex-wrap gap-2 mt-6">
              {(github.languages || []).map((language, index) => (
                <span
                  key={index}
                  className="px-3 py-2 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 text-sm"
                >
                  {language}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* ================= SKILL EVIDENCE ================= */}

        <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 md:p-7 mt-6">
          <div>
            <p className="text-cyan-400 text-xs font-semibold uppercase tracking-wider">
              ML Evidence
            </p>

            <h2 className="text-xl md:text-2xl font-bold mt-1">
              GitHub Skill Evidence
            </h2>

            <p className="text-slate-400 text-sm mt-2">
              Technical skills detected from your GitHub repositories.
            </p>
          </div>

          {sortedSkills.length > 0 ? (
            <div className="grid md:grid-cols-2 gap-x-8 gap-y-5 mt-7">
              {sortedSkills.map(([skill, score]) => {
                const percentage = Math.min(
                  100,
                  Math.max(0, Number(score) || 0)
                );

                return (
                  <div key={skill}>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-slate-200 capitalize">
                        {skill}
                      </span>

                      <span className="text-sm font-semibold text-cyan-400">
                        {percentage}%
                      </span>
                    </div>

                    <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
                        style={{
                          width: `${percentage}%`,
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="mt-6 p-5 rounded-xl bg-slate-800/50 border border-slate-700 text-slate-400">
              No GitHub skill evidence detected.
            </div>
          )}
        </div>

        {/* ================= ML PIPELINE ================= */}

        <div className="rounded-3xl border border-cyan-500/20 bg-cyan-500/[0.04] p-6 md:p-7 mt-6">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 shrink-0 rounded-xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center text-2xl">
              🤖
            </div>

            <div>
              <p className="text-cyan-400 text-xs font-semibold uppercase tracking-wider">
                Machine Learning
              </p>

              <h2 className="text-xl font-bold mt-1">
                GitHub → ML Pipeline
              </h2>

              <p className="text-slate-400 mt-2 leading-relaxed">
                GitHub metrics are converted into ML features and
                combined with resume and assessment data for
                Career Readiness prediction.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mt-6">
            <FeatureItem
              name="Repositories"
              value={github.github_repo_count}
            />

            <FeatureItem
              name="Languages"
              value={github.github_language_count}
            />

            <FeatureItem
              name="Stars"
              value={github.github_star_count}
            />

            <FeatureItem
              name="Forks"
              value={github.github_fork_count}
            />

            <FeatureItem
              name="Projects"
              value={github.github_project_count}
            />

            <FeatureItem
              name="Activity"
              value={`${activity}/100`}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

/* =========================
   METRIC CARD
========================= */

function MetricCard({
  icon,
  title,
  value,
  suffix = "",
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5 hover:border-slate-700 transition">
      <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-xl">
        {icon}
      </div>

      <p className="text-slate-500 text-xs uppercase tracking-wider mt-5">
        {title}
      </p>

      <h2 className="text-2xl font-bold mt-1">
        {value ?? 0}

        {suffix && (
          <span className="text-sm text-slate-500 ml-1">
            {suffix}
          </span>
        )}
      </h2>
    </div>
  );
}

/* =========================
   FEATURE ITEM
========================= */

function FeatureItem({ name, value }) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/40 px-4 py-3">
      <span className="text-slate-400 text-sm">{name}</span>
      <span className="font-semibold text-white">{value ?? 0}</span>
    </div>
  );
}
