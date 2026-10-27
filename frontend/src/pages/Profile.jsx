function Profile({ analysis }) {
  const student = analysis?.student || {
    name: "Poornachandra",
    target_role: "Backend Developer",
    cgpa: 7.7,
    location: "Bangalore",
  };

  return (
    <div className="mx-auto max-w-6xl px-6 py-8">

      {/* Header */}
      <div className="mb-8">
        <p className="text-sm text-cyan-400">
          Student Profile
        </p>

        <h1 className="mt-1 text-3xl font-bold">
          My Profile
        </h1>

        <p className="mt-2 text-slate-400">
          View your academic and career information.
        </p>
      </div>


      {/* Profile Header */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <div className="flex flex-col gap-5 md:flex-row md:items-center">

          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-cyan-400 text-3xl font-bold text-slate-950">
            {student.name?.charAt(0)?.toUpperCase() || "P"}
          </div>

          <div>
            <h2 className="text-2xl font-bold">
              {student.name}
            </h2>

            <p className="mt-1 text-slate-400">
              {student.target_role}
            </p>

            <p className="mt-1 text-sm text-slate-500">
              {student.location}
            </p>
          </div>

        </div>

      </div>


      {/* Information */}
      <div className="mt-6 grid gap-6 md:grid-cols-2">

        <ProfileCard
          title="Personal Information"
          items={[
            ["Full Name", student.name],
            ["Location", student.location],
          ]}
        />

        <ProfileCard
          title="Academic Information"
          items={[
            ["Degree", "Bachelor of Computer Application"],
            ["CGPA", `${student.cgpa}/10`],
          ]}
        />

        <ProfileCard
          title="Career Information"
          items={[
            ["Target Role", student.target_role],
            ["Career Focus", "Software Development"],
          ]}
        />

        <ProfileCard
          title="Skill Summary"
          items={[
            [
              "Resume Skills",
              analysis?.resume_analysis?.skill_count || 0,
            ],
            [
              "Projects",
              analysis?.resume_analysis?.project_count || 0,
            ],
          ]}
        />

      </div>


      {/* Analysis status */}
      <div className="mt-6 rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6">

        <h3 className="text-lg font-semibold text-cyan-400">
          AI Analysis Status
        </h3>

        <p className="mt-2 text-sm text-slate-400">
          Your profile information is used by SkillPath AI
          during the career readiness analysis.
        </p>

        <div className="mt-4 grid gap-4 sm:grid-cols-3">

          <Status
            label="Profile"
            value="Available"
          />

          <Status
            label="Resume"
            value={
              analysis
                ? "Analyzed"
                : "Not analyzed"
            }
          />

          <Status
            label="ML Prediction"
            value={
              analysis
                ? "Available"
                : "Not available"
            }
          />

        </div>

      </div>

    </div>
  );
}


function ProfileCard({
  title,
  items,
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <div className="mt-5 space-y-4">

        {items.map(([label, value]) => (

          <div
            key={label}
            className="flex items-center justify-between border-b border-slate-800 pb-3"
          >

            <span className="text-sm text-slate-400">
              {label}
            </span>

            <span className="text-sm font-medium text-white">
              {value}
            </span>

          </div>

        ))}

      </div>

    </div>
  );
}


function Status({
  label,
  value,
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">

      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-sm font-medium text-green-400">
        ✓ {value}
      </p>

    </div>
  );
}


export default Profile;