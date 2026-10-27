import { useCallback, useEffect, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import AnalyzeStudent from "./pages/AnalyzeStudent";
import Sidebar from "./components/Sidebar";
import Profile from "./pages/Profile";
import Resume from "./pages/Resume";
import Assessment from "./pages/Assessment";
import GitHub from "./pages/GitHub";
import Analytics from "./pages/Analytics";
import Recommendations from "./pages/Recommendations";
import Settings from "./pages/Settings";
import RoleSelector from "./components/RoleSelector";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { useAuth } from "./context/AuthContext";
import api from "./services/api";

export default function App() {
  const { token } = useAuth();

  return (
    <Routes>
      <Route
        path="/login"
        element={token ? <Navigate to="/" replace /> : <Login />}
      />
      <Route
        path="/register"
        element={token ? <Navigate to="/" replace /> : <Register />}
      />
      <Route
        path="*"
        element={token ? <SkillPathDashboardApp /> : <Navigate to="/login" replace />}
      />
    </Routes>
  );
}

function SkillPathDashboardApp() {
  const [showAnalyze, setShowAnalyze] = useState(false);
  const [selectedRole, setSelectedRole] = useState("Backend Developer");

  const [activePage, setActivePage] =
    useState("dashboard");

  // Real ML analysis result
  const [analysis, setAnalysis] = useState(null);
  const [assessment, setAssessment] = useState(null);

  function handleAnalysisComplete(result) {
    console.log("REAL ML RESULT:", result);

    setAnalysis(result);
    if (result?.student?.target_role) {
      setSelectedRole(result.student.target_role);
    }

    if (result?.student_id) {
      localStorage.setItem(
        "skillpath_student_id",
        result.student_id
      );
    }

    setShowAnalyze(false);
  }

  // Open analysis form
  if (showAnalyze) {
    return (
      <AnalyzeStudent
        assessment={assessment}
        onAnalysisComplete={handleAnalysisComplete}
      />
    );
  }

  return (
    <Dashboard
      analysis={analysis}
      setAnalysis={setAnalysis}
      selectedRole={selectedRole}
      setSelectedRole={setSelectedRole}
      onNewAnalysis={() => setShowAnalyze(true)}
      onAssessmentComplete={setAssessment}
      activePage={activePage}
      setActivePage={setActivePage}
    />
  );
}


/* ============================================================
   DASHBOARD
============================================================ */

function Dashboard({
  analysis,
  setAnalysis,
  selectedRole,
  setSelectedRole,
  onNewAnalysis,
  onAssessmentComplete,
  activePage,
  setActivePage,
}) {
  const loadSavedStudent = useCallback(async () => {
    const studentId = localStorage.getItem(
      "skillpath_student_id"
    );

    if (!studentId) {
      return;
    }

    try {
      const response = await api.get(`/api/student/${studentId}/dashboard`);

      if (response.data?.status === "success") {
        const saved = response.data;

        console.log(
          "SAVED STUDENT DASHBOARD:",
          response.data
        );

        console.log(
          "RECOMMENDATIONS:",
          response.data.recommendations
        );

        console.log(
          "SKILL GAPS:",
          response.data.role_analysis?.skill_gaps
        );

        if (saved.student?.target_role) {
          setSelectedRole(saved.student.target_role);
        }

        setAnalysis({
          status: "success",
          student_id: studentId,
          student: saved.student,
          prediction: {
            readiness_category:
              response.data.readiness?.category || "Unknown",
            readiness_score:
              response.data.readiness?.score || 0,
          },
          resume_analysis: response.data.resume,
          github_analysis: {
            github_url:
              response.data.github?.github_url || "",
            github_repo_count:
              response.data.github?.repository_count || 0,
            github_language_count:
              response.data.github?.language_count || 0,
            github_star_count:
              response.data.github?.stars || 0,
            github_fork_count:
              response.data.github?.forks || 0,
            github_project_count:
              response.data.github?.project_count ??
              response.data.github?.repository_count ??
              0,
            github_activity_score:
              response.data.github?.activity_score || 0,
            languages:
              response.data.github?.languages || [],
            skill_evidence:
              response.data.github?.skill_evidence || {},
          },
          assessment: response.data.assessment,
          explanation: response.data.explanation,
          role_analysis:
            response.data.role_analysis || {},
          recommendations: response.data.recommendations || [],
        });
      }
    } catch (error) {
      console.error(
        "Failed to load saved student:",
        error
      );
    }
  }, [setAnalysis, setSelectedRole]);

  useEffect(() => {
    loadSavedStudent();
  }, [loadSavedStudent]);

  /*
    Demo data is used until the student performs
    the first real analysis.
  */

  const student = analysis?.student || {
    name: "Poornachandra",
    target_role: "Backend Developer",
    cgpa: 7.7,
    location: "Bangalore",
  };

  const prediction = analysis?.prediction || {
    readiness_score: 48.1,
    readiness_category: "Medium",
  };

  const resume = analysis?.resume_analysis || {
    skill_count: 17,
    project_count: 3,
    certification_count: 3,
    internship_count: 0,
  };

  const github = analysis?.github_analysis || {
    github_repo_count: 7,
    github_language_count: 5,
    github_star_count: 4,
    github_project_count: 7,
    github_activity_score: 89,
  };

  const assessment = analysis?.assessment || {
    technical_score: 75,
    aptitude_score: 85,
    problem_solving_score: 80,
    communication_score: 75,
    interview_confidence_score: 95,
  };

  const roleAnalysis = analysis?.role_analysis || {
    role: "Backend Developer",
    role_alignment: 40.12,
    skill_gaps: [
      {
        skill: "SQL",
        gap: 60,
      },
      {
        skill: "Git",
        gap: 40,
      },
      {
        skill: "REST API",
        gap: 35,
      },
      {
        skill: "Node.js",
        gap: 25,
      },
      {
        skill: "MongoDB",
        gap: 25,
      },
      {
        skill: "Python",
        gap: 5,
      },
    ],
  };

  const explanation = analysis?.explanation || {
    top_factors: [
      {
        feature: "dsa_score",
        impact: -0.1632,
        direction: "negative",
      },
      {
        feature: "internship_count",
        impact: -0.0804,
        direction: "negative",
      },
      {
        feature: "project_count",
        impact: -0.0368,
        direction: "negative",
      },
      {
        feature: "github_activity_score",
        impact: 0.0311,
        direction: "positive",
      },
      {
        feature: "resume_skill_count",
        impact: 0.0238,
        direction: "positive",
      },
      {
        feature: "communication_score",
        impact: 0.0181,
        direction: "positive",
      },
    ],
  };

  const recommendations =
    analysis?.recommendations || [
      {
        skill: "SQL",
        gap: 60,
        priority: "High",
      },
      {
        skill: "Git",
        gap: 40,
        priority: "High",
      },
      {
        skill: "REST API",
        gap: 35,
        priority: "Medium",
      },
      {
        skill: "Node.js",
        gap: 25,
        priority: "Medium",
      },
      {
        skill: "MongoDB",
        gap: 25,
        priority: "Medium",
      },
    ];

  if (activePage === "profile") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        <div className="ml-64 min-h-screen">
          <Profile analysis={analysis} />
        </div>
      </div>
    );
  }

  if (activePage === "resume") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        <div className="ml-64 min-h-screen">
          <Resume
            analysis={analysis}
            onNewAnalysis={onNewAnalysis}
          />
        </div>
      </div>
    );
  }

  if (activePage === "assessment") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        <div className="ml-64 min-h-screen">
          <Assessment
            onAssessmentComplete={(result) => {
              console.log(
                "ASSESSMENT RESULT:",
                result
              );

              onAssessmentComplete(result);
            }}
          />
        </div>
      </div>
    );
  }

  if (activePage === "github") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        <div className="ml-64 min-h-screen">
          <GitHub
            analysis={analysis}
          />
        </div>
      </div>
    );
  }

  if (activePage === "analytics") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        <div className="ml-64 min-h-screen">
          <Analytics
            analysis={analysis}
          />
        </div>
      </div>
    );
  }

  if (activePage === "recommendations") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        <div className="ml-64 min-h-screen">
          <Recommendations />
        </div>
      </div>
    );
  }

  if (activePage === "settings") {
    return (
      <div className="min-h-screen bg-slate-950 text-white">
        <Sidebar
          activePage={activePage}
          setActivePage={setActivePage}
        />

        <div className="ml-64 min-h-screen">
          <Settings
            key={JSON.stringify([
              analysis?.student?.name,
              analysis?.student?.location,
              analysis?.student?.target_role,
            ])}
            analysis={analysis}
            setAnalysis={setAnalysis}
            setSelectedRole={setSelectedRole}
            onClearAnalysis={() => {
              setAnalysis(null);
              setSelectedRole("Backend Developer");
            }}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      <div className="ml-64 min-h-screen">

      {/* ====================================================
          HEADER
      ==================================================== */}

      <header className="border-b border-slate-800 bg-slate-950/90">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">

          <div>
            <h1 className="text-2xl font-bold text-cyan-400">
              SkillPath AI
            </h1>

            <p className="text-xs text-slate-400">
              AI Career Readiness Platform
            </p>
          </div>

          <div className="flex items-center gap-4">

            <button
              onClick={onNewAnalysis}
              className="rounded-xl bg-cyan-400 px-5 py-2.5 text-sm font-bold text-slate-950 transition hover:bg-cyan-300"
            >
              + New Analysis
            </button>

            <div className="flex items-center gap-3">

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-cyan-400 font-bold text-slate-950">
                {student.name?.charAt(0)?.toUpperCase() || "P"}
              </div>

              <div>
                <p className="text-sm font-medium">
                  {student.name}
                </p>

                <p className="text-xs text-slate-400">
                  Student
                </p>
              </div>

            </div>

          </div>

        </div>

      </header>


      {/* ====================================================
          MAIN
      ==================================================== */}

      <main className="mx-auto max-w-7xl px-6 py-8">

        {/* Welcome */}

        <section className="mb-8">

          <p className="text-sm text-cyan-400">
            Welcome back 👋
          </p>

          <h2 className="mt-1 text-3xl font-bold">
            {student.name}
          </h2>

          <p className="mt-2 text-slate-400">
            Track your career readiness and improve your skills.
          </p>

        </section>


        {/* ==================================================
            TARGET CAREER ROLE
        ================================================== */}

        <section className="mb-8">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <div className="mb-5">
              <h3 className="text-xl font-semibold">
                🎯 Career Target
              </h3>

              <p className="mt-1 text-sm text-slate-400">
                Select the role you want to prepare for. SkillPath AI will
                compare your skills with the requirements of that role.
              </p>
            </div>

            <div className="max-w-xl">
              <RoleSelector
                key={selectedRole}
                selectedRole={selectedRole}
                onRoleSelect={setSelectedRole}
              />
            </div>
          </div>
        </section>

        {/* ==================================================
            TOP CARDS
        ================================================== */}

        <section className="grid gap-5 md:grid-cols-2 lg:grid-cols-4">

          {/* Readiness */}

          <Card>

            <p className="text-sm text-slate-400">
              Career Readiness
            </p>

            <div className="mt-3 flex items-end gap-2">

              <span className="text-4xl font-bold text-cyan-400">
                {Number(
                  prediction.readiness_score || 0
                ).toFixed(1)}
              </span>

              <span className="mb-1 text-slate-400">
                / 100
              </span>

            </div>

            <span className="mt-3 inline-block rounded-full bg-yellow-500/10 px-3 py-1 text-sm text-yellow-400">
              {prediction.readiness_category}
            </span>

          </Card>


          {/* Role Alignment */}

          <Card>

            <p className="text-sm text-slate-400">
              Role Alignment
            </p>

            <p className="mt-3 text-4xl font-bold text-purple-400">
              {Number(
                roleAnalysis.role_alignment || 0
              ).toFixed(2)}
              %
            </p>

            <p className="mt-2 text-sm text-slate-400">
              {roleAnalysis.role || student.target_role}
            </p>

          </Card>


          {/* Resume */}

          <Card>

            <p className="text-sm text-slate-400">
              Resume Skills
            </p>

            <p className="mt-3 text-4xl font-bold text-green-400">
              {resume.skill_count || 0}
            </p>

            <p className="mt-2 text-sm text-slate-400">
              Skills detected
            </p>

          </Card>


          {/* GitHub */}

          <Card>

            <p className="text-sm text-slate-400">
              GitHub Projects
            </p>

            <p className="mt-3 text-4xl font-bold text-blue-400">
              {github.github_repo_count || 0}
            </p>

            <p className="mt-2 text-sm text-slate-400">
              Repositories analyzed
            </p>

          </Card>

        </section>


        {/* ==================================================
            SKILL GAPS + ASSESSMENT
        ================================================== */}

        <section className="mt-8 grid gap-6 lg:grid-cols-2">

          {/* Skill Gaps */}

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <div className="flex items-center justify-between">

              <div>

                <h3 className="text-xl font-semibold">
                  Skill Gaps
                </h3>

                <p className="mt-1 text-sm text-slate-400">
                  Skills to improve for your target role
                </p>

              </div>

              <span className="rounded-lg bg-purple-500/10 px-3 py-2 text-sm text-purple-400">
                {roleAnalysis.role}
              </span>

            </div>


            <div className="mt-6 space-y-5">

              {roleAnalysis.skill_gaps?.map(
                (item, index) => (
                  <SkillBar
                    key={index}
                    skill={item.skill}
                    gap={item.gap}
                    index={index}
                  />
                )
              )}

            </div>

          </div>


          {/* Assessment */}

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h3 className="text-xl font-semibold">
              Assessment Performance
            </h3>

            <p className="mt-1 text-sm text-slate-400">
              Your latest assessment scores
            </p>


            <div className="mt-6 space-y-5">

              <ScoreBar
                title="Technical"
                score={assessment.technical_score}
              />

              <ScoreBar
                title="Aptitude"
                score={assessment.aptitude_score}
              />

              <ScoreBar
                title="Problem Solving"
                score={assessment.problem_solving_score}
              />

              <ScoreBar
                title="Communication"
                score={assessment.communication_score}
              />

              <ScoreBar
                title="Interview Confidence"
                score={
                  assessment.interview_confidence_score
                }
              />

            </div>

          </div>

        </section>


        {/* ==================================================
            AI + RECOMMENDATIONS
        ================================================== */}

        <section className="mt-8 grid gap-6 lg:grid-cols-2">

          {/* SHAP */}

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h3 className="text-xl font-semibold">
              🤖 AI Explanation
            </h3>

            <p className="mt-1 text-sm text-slate-400">
              Factors affecting your prediction
            </p>


            <div className="mt-5 space-y-3">

              {explanation.top_factors
                ?.slice(0, 6)
                .map((factor, index) => (

                  <Factor
                    key={index}
                    name={formatFeatureName(
                      factor.feature
                    )}
                    value={factor.impact}
                    negative={
                      factor.direction === "negative" ||
                      factor.impact < 0
                    }
                  />

                ))}

            </div>

          </div>


          {/* Recommendations */}

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h3 className="text-xl font-semibold">
              📚 Recommended Learning
            </h3>

            <p className="mt-1 text-sm text-slate-400">
              Personalized recommendations based on your skill gaps
            </p>


            <div className="mt-5 space-y-3">

              {recommendations
                ?.slice(0, 6)
                .map((item, index) => (

                  <Recommendation
                    key={index}
                    skill={item.skill}
                    priority={item.priority}
                  />

                ))}

            </div>

          </div>

        </section>


        {/* ==================================================
            ADDITIONAL INFORMATION
        ================================================== */}

        <section className="mt-8 grid gap-6 md:grid-cols-3">

          <InfoCard
            title="Projects"
            value={resume.project_count}
            description="Projects detected in resume"
          />

          <InfoCard
            title="Certifications"
            value={resume.certification_count}
            description="Certifications detected"
          />

          <InfoCard
            title="GitHub Activity"
            value={`${github.github_activity_score || 0}%`}
            description="GitHub activity score"
          />

        </section>

      </main>

      </div>

    </div>
  );
}


/* ============================================================
   CARD
============================================================ */

function Card({ children }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      {children}
    </div>
  );
}


/* ============================================================
   SKILL BAR
============================================================ */

function SkillBar({
  skill,
  gap,
  index,
}) {
  const colors = [
    "bg-red-500",
    "bg-orange-500",
    "bg-yellow-500",
    "bg-blue-500",
    "bg-green-500",
    "bg-cyan-500",
  ];

  const color = colors[index % colors.length];

  return (
    <div>

      <div className="mb-2 flex justify-between text-sm">

        <span>
          {skill}
        </span>

        <span className="text-slate-400">
          Gap: {gap}
        </span>

      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-800">

        <div
          className={`h-full rounded-full ${color}`}
          style={{
            width: `${Math.max(
              Math.min(Number(gap) || 0, 100),
              5
            )}%`,
          }}
        />

      </div>

    </div>
  );
}


/* ============================================================
   SCORE BAR
============================================================ */

function ScoreBar({
  title,
  score,
}) {
  const safeScore = Math.max(
    0,
    Math.min(Number(score) || 0, 100)
  );

  return (
    <div>

      <div className="mb-2 flex justify-between text-sm">

        <span>
          {title}
        </span>

        <span className="font-medium text-cyan-400">
          {safeScore}%
        </span>

      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-800">

        <div
          className="h-full rounded-full bg-cyan-400 transition-all duration-700"
          style={{
            width: `${safeScore}%`,
          }}
        />

      </div>

    </div>
  );
}


/* ============================================================
   SHAP FACTOR
============================================================ */

function Factor({
  name,
  value,
  negative,
}) {
  const numericValue = Number(value) || 0;

  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950 p-3">

      <span className="text-sm">
        {name}
      </span>

      <span
        className={
          negative
            ? "font-medium text-red-400"
            : "font-medium text-green-400"
        }
      >
        {numericValue >= 0 ? "+" : ""}
        {numericValue.toFixed(4)}
      </span>

    </div>
  );
}


/* ============================================================
   RECOMMENDATION
============================================================ */

function Recommendation({
  skill,
  priority,
}) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950 p-4">

      <div>

        <p className="font-medium">
          {skill}
        </p>

        <p className="text-xs text-slate-400">
          Improve {skill} skills
        </p>

      </div>

      <span
        className={
          priority === "High"
            ? "rounded-full bg-red-500/10 px-3 py-1 text-xs text-red-400"
            : "rounded-full bg-yellow-500/10 px-3 py-1 text-xs text-yellow-400"
        }
      >
        {priority}
      </span>

    </div>
  );
}


/* ============================================================
   INFO CARD
============================================================ */

function InfoCard({
  title,
  value,
  description,
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

      <p className="text-sm text-slate-400">
        {title}
      </p>

      <p className="mt-2 text-3xl font-bold text-cyan-400">
        {value || 0}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {description}
      </p>

    </div>
  );
}


/* ============================================================
   FORMAT FEATURE NAME
============================================================ */

function formatFeatureName(feature) {
  if (!feature) {
    return "Unknown";
  }

  return feature
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase()
    );
}
