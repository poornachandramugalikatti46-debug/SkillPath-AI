import { useMemo } from "react";

export default function Analytics({ analysis }) {
  if (!analysis) {
    return (
      <div className="min-h-screen bg-slate-950 text-white p-6 md:p-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-cyan-400 text-xs font-bold tracking-[0.25em] uppercase">
            SkillPath AI
          </p>

          <h1 className="text-3xl md:text-4xl font-bold mt-2">
            Career Intelligence
          </h1>

          <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-900/70 p-12 text-center">
            <div className="text-5xl">📊</div>

            <h2 className="text-2xl font-bold mt-5">
              No Analytics Available
            </h2>

            <p className="text-slate-400 mt-2">
              Complete a student analysis to generate your personalized
              career analytics.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const prediction = analysis.prediction || {};
  const role = analysis.role_analysis || {};
  const assessment = analysis.assessment || {};
  const github = analysis.github_analysis || {};
  const resume = analysis.resume_analysis || {};
  const explanation = analysis.explanation || {};

  const readiness = clamp(prediction.readiness_score);
  const roleAlignment = clamp(role.role_alignment);

  const technical = clamp(assessment.technical_score);
  const aptitude = clamp(assessment.aptitude_score);
  const problemSolving = clamp(assessment.problem_solving_score);
  const communication = clamp(assessment.communication_score);
  const confidence = clamp(assessment.interview_confidence_score);

  const assessmentAverage = Math.round(
    (technical +
      aptitude +
      problemSolving +
      communication +
      confidence) /
      5
  );

  const githubActivity = clamp(github.github_activity_score);

  const skillEvidence = github.skill_evidence || {};

  const topSkills = Object.entries(skillEvidence)
    .sort(([, a], [, b]) => Number(b) - Number(a))
    .slice(0, 6);

  const gaps = role.skill_gaps || [];

  const topGaps = [...gaps]
    .sort((a, b) => Number(b.gap || 0) - Number(a.gap || 0))
    .slice(0, 5);

  const factors = explanation.top_factors || [];

  const readinessLabel =
    prediction.readiness_category || getReadinessLabel(readiness);

  const readinessMessage =
    readiness < 50
      ? "You have a strong foundation, but several skills need improvement."
      : readiness < 75
      ? "You are progressing well. Focus on your biggest skill gaps."
      : "Excellent progress. Keep strengthening your interview readiness.";

  return (
    <div className="min-h-screen bg-slate-950 text-white p-5 md:p-8">
      <div className="max-w-7xl mx-auto">

        {/* =====================================================
            HEADER
        ===================================================== */}

        <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-5 mb-8">

          <div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/50" />

              <p className="text-cyan-400 text-xs font-bold tracking-[0.25em] uppercase">
                SkillPath AI
              </p>
            </div>

            <h1 className="text-3xl md:text-5xl font-black mt-3 tracking-tight">
              Career Intelligence
            </h1>

            <p className="text-slate-400 mt-3 max-w-2xl">
              Your personalized machine-learning analysis of career
              readiness, technical skills and improvement areas.
            </p>
          </div>

          <div className="px-5 py-3 rounded-2xl border border-slate-800 bg-slate-900/70">
            <p className="text-xs text-slate-500 uppercase tracking-wider">
              Target Role
            </p>

            <p className="font-semibold text-white mt-1">
              {role.role || "Not specified"}
            </p>
          </div>
        </div>


        {/* =====================================================
            HERO ANALYTICS
        ===================================================== */}

        <div className="grid xl:grid-cols-5 gap-6">

          {/* READINESS DONUT */}

          <div className="xl:col-span-2 relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 p-7">

            <div className="absolute -top-32 -right-32 w-72 h-72 rounded-full bg-cyan-500/10 blur-3xl" />

            <div className="relative">

              <div className="flex justify-between items-start">
                <div>
                  <p className="text-cyan-400 text-xs font-bold uppercase tracking-wider">
                    ML Prediction
                  </p>

                  <h2 className="text-2xl font-bold mt-1">
                    Career Readiness
                  </h2>
                </div>

                <span className="px-3 py-1.5 rounded-full bg-cyan-400/10 border border-cyan-400/20 text-cyan-300 text-xs font-semibold">
                  {readinessLabel}
                </span>
              </div>

              <div className="flex justify-center py-8">
                <DonutChart
                  value={readiness}
                  size={230}
                  stroke={18}
                  label={`${readiness.toFixed(1)}`}
                  sublabel="/ 100"
                />
              </div>

              <p className="text-center text-slate-400 text-sm leading-relaxed">
                {readinessMessage}
              </p>

            </div>
          </div>


          {/* READINESS BREAKDOWN */}

          <div className="xl:col-span-3 rounded-3xl border border-slate-800 bg-slate-900/70 p-7">

            <div className="flex justify-between items-start">
              <div>
                <p className="text-cyan-400 text-xs font-bold uppercase tracking-wider">
                  Performance Overview
                </p>

                <h2 className="text-2xl font-bold mt-1">
                  Readiness Breakdown
                </h2>

                <p className="text-slate-500 text-sm mt-2">
                  Key signals contributing to your career profile.
                </p>
              </div>

              <div className="text-3xl">
                ✦
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-4 mt-7">

              <InsightCard
                title="Assessment"
                value={assessmentAverage}
                icon="🧠"
                description="Overall assessment"
              />

              <InsightCard
                title="Role Match"
                value={roleAlignment}
                icon="🎯"
                description="Target role alignment"
              />

              <InsightCard
                title="GitHub Activity"
                value={githubActivity}
                icon="🐙"
                description="Developer activity"
              />

              <InsightCard
                title="Resume Skills"
                value={resume.skill_count || 0}
                icon="📄"
                description="Detected skills"
                suffix=" skills"
                noPercent
              />

            </div>

            <div className="mt-7 grid grid-cols-5 gap-2">

              <MiniScore label="Technical" value={technical} />
              <MiniScore label="Aptitude" value={aptitude} />
              <MiniScore label="DSA" value={problemSolving} />
              <MiniScore label="Communication" value={communication} />
              <MiniScore label="Confidence" value={confidence} />

            </div>

          </div>
        </div>


        {/* =====================================================
            ASSESSMENT DONUTS
        ===================================================== */}

        <section className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/70 p-7">

          <SectionHeader
            eyebrow="Assessment Intelligence"
            title="Your Interview Readiness"
            description="How you performed across the five assessment dimensions."
          />

          <div className="grid grid-cols-2 md:grid-cols-5 gap-6 mt-8">

            <SmallDonut title="Technical" value={technical} />
            <SmallDonut title="Aptitude" value={aptitude} />
            <SmallDonut title="Problem Solving" value={problemSolving} />
            <SmallDonut title="Communication" value={communication} />
            <SmallDonut title="Confidence" value={confidence} />

          </div>

        </section>


        {/* =====================================================
            SKILLS + GITHUB
        ===================================================== */}

        <div className="grid lg:grid-cols-2 gap-6 mt-6">

          {/* SKILL PROFILE */}

          <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-7">

            <SectionHeader
              eyebrow="Technical Intelligence"
              title="GitHub Skill Evidence"
              description="Skills detected from your real GitHub repositories."
            />

            {topSkills.length > 0 ? (
              <div className="mt-7 space-y-5">

                {topSkills.map(([skill, score]) => (
                  <SkillBar
                    key={skill}
                    label={formatSkill(skill)}
                    value={Number(score)}
                  />
                ))}

              </div>
            ) : (
              <EmptyState text="No GitHub skill evidence available yet." />
            )}

          </section>


          {/* RESUME PROFILE */}

          <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-7">

            <SectionHeader
              eyebrow="Resume Intelligence"
              title="Profile Strength"
              description="Evidence extracted from your resume."
            />

            <div className="grid grid-cols-2 gap-4 mt-7">

              <ProfileMetric
                value={resume.skill_count}
                label="Skills"
                icon="⚡"
              />

              <ProfileMetric
                value={resume.project_count}
                label="Projects"
                icon="🚀"
              />

              <ProfileMetric
                value={resume.internship_count}
                label="Internships"
                icon="💼"
              />

              <ProfileMetric
                value={resume.certification_count}
                label="Certifications"
                icon="🏆"
              />

            </div>

            <div className="mt-5 rounded-2xl bg-slate-950/60 border border-slate-800 p-5">

              <div className="flex justify-between">
                <span className="text-slate-400">
                  Experience
                </span>

                <span className="font-bold">
                  {resume.experience_months || 0} months
                </span>
              </div>

            </div>

          </section>

        </div>


        {/* =====================================================
            SKILL GAP
        ===================================================== */}

        <section className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/70 p-7">

          <SectionHeader
            eyebrow="Career Gap Analysis"
            title="What You Need To Improve"
            description="The biggest differences between your current skills and your target role."
          />

          {topGaps.length > 0 ? (
            <div className="grid md:grid-cols-2 gap-5 mt-7">

              {topGaps.map((gap, index) => (
                <GapCard
                  key={index}
                  skill={gap.skill}
                  current={gap.student_score}
                  required={gap.required_score}
                  gap={gap.gap}
                />
              ))}

            </div>
          ) : (
            <EmptyState text="No major skill gaps detected." />
          )}

        </section>


        {/* =====================================================
            SHAP
        ===================================================== */}

        <section className="mt-6 rounded-3xl border border-slate-800 bg-slate-900/70 p-7">

          <SectionHeader
            eyebrow="Explainable AI"
            title="Why Did The Model Predict This?"
            description="SHAP explains which features influenced your ML prediction."
          />

          {factors.length > 0 ? (
            <div className="mt-7 space-y-4">

              {factors.slice(0, 6).map((factor, index) => (
                <ShapBar
                  key={index}
                  feature={factor.feature}
                  impact={Number(factor.impact || 0)}
                  direction={factor.direction}
                />
              ))}

            </div>
          ) : (
            <EmptyState text="SHAP explanation is not available yet." />
          )}

        </section>


        {/* =====================================================
            FINAL INSIGHT
        ===================================================== */}

        <div className="mt-6 rounded-3xl border border-cyan-500/20 bg-gradient-to-r from-cyan-500/[0.08] to-blue-500/[0.05] p-7">

          <div className="flex gap-5 items-start">

            <div className="w-12 h-12 shrink-0 rounded-2xl bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center text-2xl">
              🤖
            </div>

            <div>

              <p className="text-cyan-400 text-xs font-bold uppercase tracking-wider">
                AI Career Insight
              </p>

              <h2 className="text-xl md:text-2xl font-bold mt-1">
                Your next improvement should be targeted.
              </h2>

              <p className="text-slate-400 mt-2 leading-relaxed">
                Your dashboard combines resume NLP, GitHub evidence,
                assessments, role matching and explainable ML to
                identify where you should focus next.
              </p>

            </div>

          </div>

        </div>

      </div>
    </div>
  );
}


/* =========================================================
   DONUT CHART
========================================================= */

function DonutChart({
  value,
  size = 200,
  stroke = 18,
  label,
  sublabel,
}) {
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (value / 100) * circumference;

  return (
    <div
      className="relative"
      style={{ width: size, height: size }}
    >
      <svg
        width={size}
        height={size}
        className="-rotate-90"
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={stroke}
          className="text-slate-800"
        />

        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          className="text-cyan-400 transition-all duration-1000"
        />
      </svg>

      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-black">
          {label}
        </span>

        <span className="text-slate-500 text-sm">
          {sublabel}
        </span>
      </div>
    </div>
  );
}


/* =========================================================
   SMALL DONUT
========================================================= */

function SmallDonut({ title, value }) {
  return (
    <div className="flex flex-col items-center">

      <DonutChart
        value={value}
        size={130}
        stroke={11}
        label={`${Math.round(value)}`}
        sublabel="%"
      />

      <p className="text-sm text-slate-300 font-medium mt-3 text-center">
        {title}
      </p>

    </div>
  );
}


/* =========================================================
   INSIGHT CARD
========================================================= */

function InsightCard({
  title,
  value,
  icon,
  description,
  suffix = "%",
  noPercent = false,
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-5">

      <div className="flex justify-between">
        <span className="text-2xl">
          {icon}
        </span>

        <span className="text-xs text-slate-600">
          LIVE
        </span>
      </div>

      <p className="text-slate-500 text-xs uppercase tracking-wider mt-5">
        {title}
      </p>

      <p className="text-3xl font-black mt-1">
        {Number(value || 0).toFixed(noPercent ? 0 : 0)}
        {!noPercent && (
          <span className="text-sm text-slate-500 ml-1">
            {suffix}
          </span>
        )}
      </p>

      <p className="text-xs text-slate-600 mt-1">
        {description}
      </p>

    </div>
  );
}


/* =========================================================
   MINI SCORE
========================================================= */

function MiniScore({ label, value }) {
  return (
    <div className="text-center">

      <div className="text-xs text-slate-500 truncate">
        {label}
      </div>

      <div className="text-sm font-bold text-cyan-400 mt-1">
        {Math.round(value)}%
      </div>

    </div>
  );
}


/* =========================================================
   SKILL BAR
========================================================= */

function SkillBar({ label, value }) {
  const score = clamp(value);

  return (
    <div>

      <div className="flex justify-between items-center mb-2">

        <span className="text-sm font-medium text-slate-300">
          {label}
        </span>

        <span className="text-sm font-bold text-cyan-400">
          {score}%
        </span>

      </div>

      <div className="h-2.5 rounded-full bg-slate-800 overflow-hidden">

        <div
          className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-700"
          style={{ width: `${score}%` }}
        />

      </div>

    </div>
  );
}


/* =========================================================
   PROFILE METRIC
========================================================= */

function ProfileMetric({ value, label, icon }) {
  return (
    <div className="rounded-2xl bg-slate-950/60 border border-slate-800 p-5">

      <div className="text-2xl">
        {icon}
      </div>

      <p className="text-2xl font-black mt-4">
        {value ?? 0}
      </p>

      <p className="text-xs text-slate-500 uppercase tracking-wider mt-1">
        {label}
      </p>

    </div>
  );
}


/* =========================================================
   GAP CARD
========================================================= */

function GapCard({
  skill,
  current,
  required,
  gap,
}) {
  const currentScore = clamp(current);
  const requiredScore = clamp(required);
  const gapScore = clamp(gap);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/50 p-5">

      <div className="flex justify-between items-center">

        <div>
          <h3 className="font-bold">
            {skill}
          </h3>

          <p className="text-xs text-slate-500 mt-1">
            Current {currentScore} • Required {requiredScore}
          </p>
        </div>

        <div className="text-right">
          <p className="text-red-400 font-bold">
            -{gapScore}
          </p>

          <p className="text-[10px] text-slate-600 uppercase">
            Gap
          </p>
        </div>

      </div>

      <div className="mt-5 h-3 bg-slate-800 rounded-full overflow-hidden">

        <div
          className="h-full rounded-full bg-gradient-to-r from-red-500 to-orange-400"
          style={{ width: `${gapScore}%` }}
        />

      </div>

    </div>
  );
}


/* =========================================================
   SHAP BAR
========================================================= */

function ShapBar({
  feature,
  impact,
  direction,
}) {
  const positive = impact >= 0;
  const width = Math.min(100, Math.abs(impact) * 400);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4">

      <div className="flex items-center justify-between">

        <div>
          <p className="font-medium text-slate-200">
            {formatFeature(feature)}
          </p>

          <p
            className={`text-xs mt-1 ${
              positive
                ? "text-emerald-400"
                : "text-red-400"
            }`}
          >
            {direction || (positive ? "positive" : "negative")}
          </p>
        </div>

        <p
          className={`font-bold ${
            positive
              ? "text-emerald-400"
              : "text-red-400"
          }`}
        >
          {positive ? "+" : ""}
          {impact.toFixed(4)}
        </p>

      </div>

      <div className="mt-3 h-2 bg-slate-800 rounded-full overflow-hidden">

        <div
          className={`h-full rounded-full ${
            positive
              ? "bg-emerald-400"
              : "bg-red-400"
          }`}
          style={{
            width: `${Math.max(width, 4)}%`,
          }}
        />

      </div>

    </div>
  );
}


/* =========================================================
   SECTION HEADER
========================================================= */

function SectionHeader({
  eyebrow,
  title,
  description,
}) {
  return (
    <div>
      <p className="text-cyan-400 text-xs font-bold uppercase tracking-[0.18em]">
        {eyebrow}
      </p>

      <h2 className="text-2xl font-bold mt-1">
        {title}
      </h2>

      <p className="text-slate-500 text-sm mt-2">
        {description}
      </p>
    </div>
  );
}


/* =========================================================
   EMPTY STATE
========================================================= */

function EmptyState({ text }) {
  return (
    <div className="mt-6 rounded-2xl border border-dashed border-slate-800 p-8 text-center">
      <p className="text-slate-500">
        {text}
      </p>
    </div>
  );
}


/* =========================================================
   HELPERS
========================================================= */

function clamp(value) {
  const number = Number(value || 0);

  return Math.min(
    100,
    Math.max(0, number)
  );
}

function getReadinessLabel(score) {
  if (score < 50) return "Low";
  if (score < 75) return "Medium";
  return "High";
}

function formatSkill(skill) {
  return String(skill)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatFeature(feature) {
  return String(feature)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}