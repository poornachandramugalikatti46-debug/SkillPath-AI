import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

function Settings({
  analysis,
  setAnalysis,
  setSelectedRole,
  onClearAnalysis,
}) {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const student = analysis?.student || {};
  const studentId =
    analysis?.student_id ||
    localStorage.getItem("skillpath_student_id");

  const [name, setName] = useState(student.name || "Poornachandra");
  const [location, setLocation] = useState(student.location || "");
  const [targetRole, setTargetRole] = useState(
    student.target_role || "Backend Developer"
  );
  const [autoSave, setAutoSave] = useState(
    localStorage.getItem("skillpath_auto_save") !== "false"
  );
  const [showExplanation, setShowExplanation] = useState(
    localStorage.getItem("skillpath_show_explanation") !== "false"
  );
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!message) {
      return undefined;
    }

    const timer = setTimeout(() => setMessage(""), 2500);
    return () => clearTimeout(timer);
  }, [message]);

  async function handleSave() {
    setMessage("");
    setError("");

    if (!studentId) {
      setError(
        "No student analysis found. Please complete an analysis first."
      );
      return;
    }

    if (!name.trim()) {
      setError("Student name cannot be empty.");
      return;
    }

    if (!targetRole.trim()) {
      setError("Target career role cannot be empty.");
      return;
    }

    try {
      setSaving(true);

      const response = await api.put(
        `/api/student/${encodeURIComponent(studentId)}/settings`,
        {
          name: name.trim(),
          target_role: targetRole.trim(),
          location: location.trim(),
        }
      );

      if (response.data?.status !== "success") {
        throw new Error("The server did not confirm the settings update.");
      }

      const updatedProfile = response.data.student?.profile;
      if (!updatedProfile) {
        throw new Error("The server response did not include the updated profile.");
      }

      setAnalysis((previous) => ({
        ...previous,
        student: {
          ...(previous?.student || {}),
          ...updatedProfile,
        },
      }));
      setSelectedRole?.(updatedProfile.target_role || targetRole.trim());
      setMessage("Settings saved successfully.");
    } catch (saveError) {
      console.error("Settings save failed:", saveError);
      setError(
        saveError.response?.data?.detail ||
          saveError.message ||
          "Failed to save settings."
      );
    } finally {
      setSaving(false);
    }
  }

  function handleAutoSaveChange(value) {
    setAutoSave(value);
    localStorage.setItem("skillpath_auto_save", String(value));
  }

  function handleExplanationChange(value) {
    setShowExplanation(value);
    localStorage.setItem("skillpath_show_explanation", String(value));
  }

  function handleClearAnalysis() {
    const confirmed = window.confirm(
      "Are you sure you want to clear your saved analysis?"
    );

    if (!confirmed) {
      return;
    }

    localStorage.removeItem("skillpath_student_id");
    onClearAnalysis?.();
    setMessage("Saved student ID cleared.");
  }

  function handleLogout() {
    const confirmed = window.confirm("Are you sure you want to logout?");

    if (!confirmed) {
      return;
    }

    localStorage.removeItem("skillpath_student_id");
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-8 text-white">
      <div className="mx-auto max-w-5xl">
        <header className="mb-8">
          <h1 className="text-3xl font-bold">Settings</h1>
          <p className="mt-2 text-slate-400">
            Manage your SkillPath AI account and career preferences.
          </p>
        </header>

        {message && (
          <div
            className="mb-6 rounded-xl border border-cyan-500/20 bg-cyan-500/10 px-4 py-3 text-sm text-cyan-400"
            role="status"
          >
            ✓ {message}
          </div>
        )}

        {error && (
          <div
            className="mb-6 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400"
            role="alert"
          >
            {error}
          </div>
        )}

        <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div className="mb-6">
            <h2 className="text-xl font-semibold">👤 Profile</h2>
            <p className="mt-1 text-sm text-slate-400">
              Update your basic student information.
            </p>
          </div>

          <div className="grid gap-5 md:grid-cols-2">
            <div>
              <label
                htmlFor="settings-name"
                className="mb-2 block text-sm text-slate-400"
              >
                Student Name
              </label>
              <input
                id="settings-name"
                value={name}
                onChange={(event) => setName(event.target.value)}
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400"
                placeholder="Enter your name"
              />
            </div>

            <div>
              <label
                htmlFor="settings-location"
                className="mb-2 block text-sm text-slate-400"
              >
                Location
              </label>
              <input
                id="settings-location"
                value={location}
                onChange={(event) => setLocation(event.target.value)}
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400"
                placeholder="e.g. Bangalore"
              />
            </div>
          </div>
        </section>

        <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div className="mb-6">
            <h2 className="text-xl font-semibold">
              🎯 Career Preferences
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              Choose the role you want SkillPath AI to analyze.
            </p>
          </div>

          <div>
            <label
              htmlFor="settings-target-role"
              className="mb-2 block text-sm text-slate-400"
            >
              Target Career Role
            </label>
            <input
              id="settings-target-role"
              value={targetRole}
              onChange={(event) => setTargetRole(event.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-white outline-none transition focus:border-cyan-400"
              placeholder="e.g. ML Engineer"
            />
            <p className="mt-2 text-xs text-slate-500">
              Examples: Software Engineer, Backend Developer, ML Engineer,
              Data Scientist, Cloud Engineer.
            </p>
          </div>
        </section>

        <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div className="mb-6">
            <h2 className="text-xl font-semibold">
              🤖 Analysis Preferences
            </h2>
            <p className="mt-1 text-sm text-slate-400">
              Control your SkillPath AI preferences.
            </p>
          </div>

          <ToggleSetting
            title="Auto-save analysis"
            description="Keep your latest analysis available on the dashboard."
            enabled={autoSave}
            onChange={handleAutoSaveChange}
          />

          <div className="my-5 border-t border-slate-800" />

          <ToggleSetting
            title="Show AI explanations"
            description="Display the factors affecting your readiness prediction."
            enabled={showExplanation}
            onChange={handleExplanationChange}
          />
        </section>

        <div className="mb-8 flex justify-end">
          <button
            type="button"
            onClick={handleSave}
            disabled={saving}
            className="rounded-xl bg-cyan-400 px-7 py-3 text-sm font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Settings"}
          </button>
        </div>

        <section className="mb-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-xl font-semibold">🗄️ Data &amp; Security</h2>
          <p className="mt-1 text-sm text-slate-400">
            Manage your saved SkillPath AI data.
          </p>

          <div className="mt-6 flex flex-wrap gap-4">
            <button
              type="button"
              onClick={handleClearAnalysis}
              className="rounded-xl border border-red-500/30 bg-red-500/10 px-5 py-3 text-sm font-medium text-red-400 transition hover:bg-red-500/20"
            >
              Clear Saved Analysis
            </button>

            <button
              type="button"
              onClick={handleLogout}
              className="rounded-xl border border-slate-700 bg-slate-950 px-5 py-3 text-sm font-medium text-slate-300 transition hover:bg-slate-800 hover:text-white"
            >
              Logout
            </button>
          </div>
        </section>

        <footer className="pb-8 text-center">
          <p className="text-xs text-slate-600">
            SkillPath AI • AI Career Readiness Platform
          </p>
        </footer>
      </div>
    </div>
  );
}

function ToggleSetting({
  title,
  description,
  enabled,
  onChange,
}) {
  return (
    <div className="flex items-center justify-between gap-6">
      <div>
        <h3 className="font-medium">{title}</h3>
        <p className="mt-1 max-w-xl text-sm text-slate-400">
          {description}
        </p>
      </div>

      <button
        type="button"
        role="switch"
        aria-checked={enabled}
        aria-label={title}
        onClick={() => onChange(!enabled)}
        className={`relative h-7 w-12 flex-shrink-0 rounded-full transition ${
          enabled ? "bg-cyan-400" : "bg-slate-700"
        }`}
      >
        <span
          className={`absolute top-1 h-5 w-5 rounded-full bg-white transition ${
            enabled ? "left-6" : "left-1"
          }`}
        />
      </button>
    </div>
  );
}

export default Settings;
