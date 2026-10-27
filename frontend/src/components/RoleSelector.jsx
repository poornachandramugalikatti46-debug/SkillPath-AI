import { useEffect, useState } from "react";
import api from "../services/api";

function RoleSelector({
  selectedRole,
  onRoleSelect,
}) {
  const [query, setQuery] = useState(selectedRole || "");
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      return undefined;
    }

    let active = true;

    const searchRoles = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await api.get("/api/roles/search", {
          params: {
            q: trimmedQuery,
            limit: 10,
          },
        });

        if (active) {
          setRoles(response.data?.roles || []);
        }
      } catch (searchError) {
        if (active) {
          console.error("Role search failed:", searchError);
          setError("Unable to search roles.");
          setRoles([]);
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    const timer = setTimeout(searchRoles, 300);

    return () => {
      active = false;
      clearTimeout(timer);
    };
  }, [query]);

  function handleSelect(role) {
    setQuery(role);
    setShowResults(false);
    onRoleSelect?.(role);
  }

  return (
    <div className="relative">
      <label
        htmlFor="target-career-role"
        className="mb-2 block text-sm font-medium text-slate-300"
      >
        🎯 Target Career Role
      </label>

      <div className="relative">
        <input
          id="target-career-role"
          type="text"
          value={query}
          onChange={(event) => {
            setQuery(event.target.value);
            setRoles([]);
            setError("");
            setLoading(false);
            setShowResults(true);
          }}
          onFocus={() => {
            if (query.trim()) {
              setShowResults(true);
            }
          }}
          onKeyDown={(event) => {
            if (event.key === "Escape") {
              setShowResults(false);
            }
          }}
          placeholder="Search career role..."
          autoComplete="off"
          aria-autocomplete="list"
          aria-expanded={showResults && Boolean(query.trim())}
          aria-controls="target-career-role-results"
          aria-describedby={error ? "target-career-role-error" : undefined}
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 pr-10 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400"
        />

        {loading && (
          <div
            className="absolute right-4 top-1/2 -translate-y-1/2"
            aria-label="Searching roles"
          >
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-600 border-t-cyan-400" />
          </div>
        )}
      </div>

      {selectedRole && (
        <div className="mt-3 flex items-center justify-between rounded-xl border border-cyan-500/20 bg-cyan-500/5 px-4 py-3">
          <div>
            <p className="text-xs text-slate-400">Selected Role</p>
            <p className="mt-1 font-medium text-cyan-400">{selectedRole}</p>
          </div>

          <span className="rounded-full bg-cyan-400/10 px-3 py-1 text-xs text-cyan-400">
            Selected
          </span>
        </div>
      )}

      {showResults && query.trim() && (
        <div
          id="target-career-role-results"
          role="listbox"
          className="absolute left-0 right-0 z-50 mt-2 max-h-72 overflow-y-auto rounded-xl border border-slate-700 bg-slate-900 shadow-2xl"
        >
          {loading && (
            <div className="px-4 py-3 text-sm text-slate-400">
              Searching roles...
            </div>
          )}

          {!loading &&
            roles.map((item) => (
              <button
                key={item.role}
                type="button"
                role="option"
                aria-selected={item.role === selectedRole}
                onClick={() => handleSelect(item.role)}
                className="block w-full border-b border-slate-800 px-4 py-3 text-left text-sm text-slate-200 transition last:border-b-0 hover:bg-slate-800 hover:text-cyan-400"
              >
                {item.role}
              </button>
            ))}

          {!loading && !error && roles.length === 0 && (
            <div className="px-4 py-4 text-sm text-slate-400">
              No matching roles found.
            </div>
          )}
        </div>
      )}

      {error && (
        <p
          id="target-career-role-error"
          className="mt-2 text-xs text-red-400"
          role="alert"
        >
          {error}
        </p>
      )}
    </div>
  );
}

export default RoleSelector;
