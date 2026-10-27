function Resume({ analysis, onNewAnalysis }) {
  const resume = analysis?.resume_analysis;

  return (
    <div className="mx-auto max-w-6xl px-6 py-8">

      {/* Header */}
      <div className="mb-8">
        <p className="text-sm text-cyan-400">
          Resume Intelligence
        </p>

        <h1 className="mt-1 text-3xl font-bold">
          Resume Analysis
        </h1>

        <p className="mt-2 text-slate-400">
          AI-powered analysis of your resume skills, projects,
          certifications and experience.
        </p>
      </div>


      {!resume ? (
        /* Empty state */
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-10 text-center">

          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-cyan-400/10 text-4xl">
            📄
          </div>

          <h2 className="mt-5 text-2xl font-semibold">
            No Resume Analysis Yet
          </h2>

          <p className="mx-auto mt-2 max-w-lg text-slate-400">
            Upload your resume and run a career analysis to
            automatically extract your skills, projects,
            certifications and experience.
          </p>

          <button
            onClick={onNewAnalysis}
            className="mt-6 rounded-xl bg-cyan-400 px-6 py-3 font-bold text-slate-950 transition hover:bg-cyan-300"
          >
            Analyze My Resume 🚀
          </button>

        </div>
      ) : (
        <>
          {/* Summary cards */}
          <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-4">

            <SummaryCard
              title="Skills"
              value={resume.skill_count}
              icon="🧠"
            />

            <SummaryCard
              title="Projects"
              value={resume.project_count}
              icon="💻"
            />

            <SummaryCard
              title="Certifications"
              value={resume.certification_count}
              icon="🏆"
            />

            <SummaryCard
              title="Internships"
              value={resume.internship_count}
              icon="💼"
            />

          </div>


          {/* Skills */}
          <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              🧠 Detected Skills
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Skills identified by the resume NLP pipeline.
            </p>

            <div className="mt-5 flex flex-wrap gap-3">

              {resume.skills?.map((skill) => (

                <span
                  key={skill}
                  className="rounded-full border border-cyan-500/20 bg-cyan-500/10 px-4 py-2 text-sm text-cyan-300"
                >
                  {skill}
                </span>

              ))}

            </div>

          </section>


          {/* Projects + Certifications */}
          <div className="mt-6 grid gap-6 lg:grid-cols-2">

            {/* Projects */}
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

              <h2 className="text-xl font-semibold">
                💻 Projects
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Projects detected from your resume.
              </p>

              <div className="mt-5 rounded-xl bg-slate-950 p-4">

                <p className="whitespace-pre-line text-sm leading-7 text-slate-300">
                  {resume.projects_section ||
                    "No project section detected."}
                </p>

              </div>

            </section>


            {/* Certifications */}
            <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

              <h2 className="text-xl font-semibold">
                🏆 Certifications
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Certifications detected from your resume.
              </p>

              <div className="mt-5 rounded-xl bg-slate-950 p-4">

                <p className="whitespace-pre-line text-sm leading-7 text-slate-300">
                  {resume.certifications_section ||
                    "No certification section detected."}
                </p>

              </div>

            </section>

          </div>


          {/* Experience */}
          <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              💼 Experience
            </h2>

            <div className="mt-5 grid gap-4 md:grid-cols-3">

              <Metric
                label="Internships"
                value={resume.internship_count || 0}
              />

              <Metric
                label="Experience"
                value={`${resume.experience_months || 0} months`}
              />

              <Metric
                label="Education Entries"
                value={resume.education_count || 1}
              />

            </div>

          </section>


          {/* Text statistics */}
          <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">

            <h2 className="text-xl font-semibold">
              📊 Resume Statistics
            </h2>

            <div className="mt-5 grid gap-4 md:grid-cols-3">

              <Metric
                label="Detected Skills"
                value={resume.skill_count || 0}
              />

              <Metric
                label="Projects"
                value={resume.project_count || 0}
              />

              <Metric
                label="Resume Text"
                value={`${resume.text_length || 0} characters`}
              />

            </div>

          </section>

        </>
      )}

    </div>
  );
}


/* ============================================================
   SUMMARY CARD
============================================================ */

function SummaryCard({
  title,
  value,
  icon,
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

      <div className="flex items-center justify-between">

        <p className="text-sm text-slate-400">
          {title}
        </p>

        <span className="text-xl">
          {icon}
        </span>

      </div>

      <p className="mt-3 text-4xl font-bold text-cyan-400">
        {value || 0}
      </p>

    </div>
  );
}


/* ============================================================
   METRIC
============================================================ */

function Metric({
  label,
  value,
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">

      <p className="text-sm text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-xl font-semibold text-white">
        {value}
      </p>

    </div>
  );
}


export default Resume;