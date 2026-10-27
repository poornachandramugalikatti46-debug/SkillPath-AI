import { useEffect, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../services/api";

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [skillGaps, setSkillGaps] = useState([]);
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadRecommendations();
  }, []);

  async function loadRecommendations() {
    try {
      setLoading(true);
      setError("");

      const studentId = localStorage.getItem(
        "skillpath_student_id"
      );

      console.log("SKILLPATH STUDENT ID:", studentId);

      if (!studentId) {
        setError(
          "No student analysis found. Please create a new analysis first."
        );
        return;
      }

      const response = await axios.get(
        `${API_BASE_URL}/api/student/${studentId}/dashboard`
      );

      console.log("DASHBOARD API RESPONSE:", response.data);

      if (response.data?.status !== "success") {
        throw new Error(
          "Student dashboard could not be loaded."
        );
      }

      const roleAnalysis = response.data.role_analysis || {};
      const skillGaps = Array.isArray(roleAnalysis.skill_gaps)
        ? roleAnalysis.skill_gaps
        : [];
      const backendRecommendations = Array.isArray(
        response.data.recommendations
      )
        ? response.data.recommendations
        : Array.isArray(roleAnalysis.recommendations)
        ? roleAnalysis.recommendations
        : [];

      console.log(
        "BACKEND RECOMMENDATIONS:",
        backendRecommendations
      );
      console.log("BACKEND SKILL GAPS:", skillGaps);

      setSkillGaps(skillGaps);
      setRole(
        roleAnalysis.role ||
          response.data.student?.target_role ||
          response.data.profile?.target_role ||
          ""
      );

      if (backendRecommendations.length > 0) {
        setRecommendations(backendRecommendations);
        return;
      }

      if (skillGaps.length > 0) {
        setRecommendations(
          skillGaps.map((gap) => {
            const gapScore = Number(gap.gap) || 0;

            return {
              skill: gap.skill,
              required_score: gap.required_score,
              student_score: gap.student_score,
              gap: gapScore,
              priority:
                gapScore >= 40
                  ? "High"
                  : gapScore >= 20
                  ? "Medium"
                  : "Low",
              resources: [],
            };
          })
        );
        return;
      }

      setRecommendations([]);
    } catch (err) {
      console.error("RECOMMENDATIONS ERROR:", err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Unable to load recommendations."
      );
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <PageMessage
        title="Loading Recommendations..."
        message="Loading your ML-based skill recommendations."
        icon="🤖"
      />
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 p-8 text-white">
        <div className="mx-auto max-w-5xl">
          <p className="text-sm font-medium text-cyan-400">
            SKILLPATH AI
          </p>
          <h1 className="mt-2 text-3xl font-bold">
            Personalized Recommendations 🎯
          </h1>
          <div className="mt-8 rounded-2xl border border-red-500/30 bg-red-500/10 p-6">
            <h2 className="text-lg font-semibold text-red-400">
              Unable to load recommendations
            </h2>
            <p className="mt-2 text-slate-400">{error}</p>
            <button
              onClick={loadRecommendations}
              className="mt-5 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  const highPriorityCount = recommendations.filter(
    (item) => String(item.priority || "").toLowerCase() === "high"
  ).length;
  const learningPlanCount = recommendations.reduce(
    (total, item) =>
      total +
      (Array.isArray(item.resources) ? item.resources.length : 0),
    0
  );

  return (
    <div className="min-h-screen bg-slate-950 p-8 text-white">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8">
          <p className="text-sm font-medium text-cyan-400">
            SKILLPATH AI
          </p>
          <h1 className="mt-2 text-3xl font-bold">
            Personalized Recommendations 🎯
          </h1>
          <p className="mt-2 text-slate-400">
            Improve the skills identified by your ML-based skill-gap analysis.
          </p>
          {role && (
            <p className="mt-2 text-slate-500">
              Target Role: <span className="text-cyan-400">{role}</span>
            </p>
          )}
        </div>

        <div className="mb-8 grid gap-5 md:grid-cols-3">
          <SummaryCard
            icon="⚠️"
            title="Skills to Improve"
            value={skillGaps.length || recommendations.length}
          />
          <SummaryCard
            icon="🔥"
            title="High Priority"
            value={highPriorityCount}
          />
          <SummaryCard
            icon="📚"
            title="Learning Plans"
            value={learningPlanCount}
          />
        </div>

        {skillGaps.length > 0 && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold">Your Skill Gaps</h2>
            <p className="mt-1 text-slate-400">
              Skills where your current evidence is below the target role requirement.
            </p>

            <div className="mt-5 grid gap-5 md:grid-cols-2">
              {skillGaps.map((gap, index) => {
                const required = Number(gap.required_score) || 0;
                const current = Number(gap.student_score) || 0;
                const difference = Number(
                  gap.gap ?? Math.max(required - current, 0)
                ) || 0;
                const progress =
                  required > 0
                    ? Math.min(Math.max((current / required) * 100, 0), 100)
                    : 0;

                return (
                  <div
                    key={`${gap.skill}-${index}`}
                    className="rounded-2xl border border-slate-800 bg-slate-900 p-6"
                  >
                    <div className="mb-4 flex items-center justify-between gap-3">
                      <h3 className="text-xl font-semibold capitalize">
                        {gap.skill || "Unknown Skill"}
                      </h3>
                      <span className="rounded-full border border-red-500/20 bg-red-500/10 px-3 py-1 text-sm text-red-300">
                        Gap {difference}
                      </span>
                    </div>

                    <div className="mb-2 flex justify-between text-sm">
                      <span className="text-slate-400">Current: {current}</span>
                      <span className="text-cyan-400">Required: {required}</span>
                    </div>

                    <div className="h-3 overflow-hidden rounded-full bg-slate-800">
                      <div
                        className="h-full rounded-full bg-cyan-400"
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {recommendations.length === 0 && skillGaps.length === 0 ? (
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-10 text-center">
            <div className="text-5xl">🎉</div>
            <h2 className="mt-4 text-xl font-semibold">
              No Skill Gaps Found
            </h2>
            <p className="mt-2 text-slate-400">
              The current analysis did not generate any recommendations.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {recommendations.map((recommendation, index) => (
              <RecommendationCard
                key={index}
                recommendation={recommendation}
                index={index}
              />
            ))}
          </div>
        )}

        <div className="mt-8 rounded-2xl border border-cyan-500/30 bg-cyan-500/10 p-6">
          <h2 className="text-xl font-semibold text-cyan-300">
            How these recommendations are generated
          </h2>
          <p className="mt-2 leading-relaxed text-slate-400">
            SkillPath AI compares your detected skills with the required skills
            for the selected target role and generates recommendations from the
            resulting gaps.
          </p>
        </div>
      </div>
    </div>
  );
}

function RecommendationCard({ recommendation, index }) {
  const skill = recommendation.skill || "Unknown Skill";
  const current = Number(recommendation.student_score || 0);
  const required = Number(recommendation.required_score || 0);
  const gap = Number(recommendation.gap || 0);
  const priority = recommendation.priority || "Low";
  const resources = recommendation.resources || [];
  const priorityClass =
    priority === "High"
      ? "border-red-500/30 bg-red-500/10 text-red-400"
      : priority === "Medium"
      ? "border-yellow-500/30 bg-yellow-500/10 text-yellow-400"
      : "border-emerald-500/30 bg-emerald-500/10 text-emerald-400";

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-cyan-500/20 bg-cyan-500/10 font-bold text-cyan-400">
            {index + 1}
          </div>
          <div>
            <h2 className="text-xl font-semibold">{skill}</h2>
            <p className="mt-1 text-sm text-slate-500">
              Skill development recommendation
            </p>
          </div>
        </div>
        <div className={`rounded-xl border px-4 py-2 font-semibold ${priorityClass}`}>
          {priority}
        </div>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        <ScoreBox label="Current Score" value={current} />
        <ScoreBox label="Required Score" value={required} />
        <ScoreBox label="Skill Gap" value={gap} />
      </div>

      <div className="mt-6">
        <div className="mb-2 flex justify-between text-sm">
          <span className="text-slate-400">Current skill level</span>
          <span className="text-cyan-400">
            {current} / {required}
          </span>
        </div>
        <div className="h-3 w-full overflow-hidden rounded-full bg-slate-800">
          <div
            className="h-full rounded-full bg-cyan-400"
            style={{ width: `${Math.min(100, Math.max(0, current))}%` }}
          />
        </div>
      </div>

      {resources.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold">Learning Resources 📚</h3>
          <div className="mt-4 grid gap-3 md:grid-cols-2">
            {resources.map((resource, resourceIndex) => (
              <ResourceCard
                key={resourceIndex}
                resource={resource}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function ScoreBox({ label, value }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-bold">{value}</p>
    </div>
  );
}

function ResourceCard({ resource }) {
  const title =
    resource.title ||
    resource.name ||
    resource.resource ||
    "Learning Resource";
  const url = resource.url || resource.link || resource.href;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
      <div className="flex items-start justify-between gap-3">
        <p className="font-medium">📘 {title}</p>
        {url && (
          <a
            href={url}
            target="_blank"
            rel="noreferrer"
            className="text-sm text-cyan-400 hover:text-cyan-300"
          >
            Open →
          </a>
        )}
      </div>
    </div>
  );
}

function SummaryCard({ icon, title, value }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="text-3xl">{icon}</div>
      <p className="mt-4 text-slate-400">{title}</p>
      <p className="mt-1 text-3xl font-bold">{value}</p>
    </div>
  );
}

function PageMessage({ title, message, icon }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
      <div className="text-center">
        <div className="mb-4 text-5xl">{icon}</div>
        <h2 className="text-xl font-semibold">{title}</h2>
        <p className="mt-2 text-slate-400">{message}</p>
      </div>
    </div>
  );
}