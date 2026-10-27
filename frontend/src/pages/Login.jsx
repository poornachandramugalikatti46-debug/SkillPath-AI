import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import "../styles/Auth.css";

function BrandLogo() {
  return (
    <Link to="/login" className="sp-brand" aria-label="SkillPath AI home">
      <span className="sp-brand-mark">
        <svg viewBox="0 0 48 48" fill="none" aria-hidden="true">
          <rect width="48" height="48" rx="14" fill="currentColor" />
          <path
            d="M12 18L24 11L36 18L24 25L12 18Z"
            stroke="white"
            strokeWidth="2.4"
            strokeLinejoin="round"
          />
          <path
            d="M16 21V29C21 34 27 34 32 29V21"
            stroke="white"
            strokeWidth="2.4"
            strokeLinecap="round"
          />
          <path
            d="M36 19V28"
            stroke="white"
            strokeWidth="2.4"
            strokeLinecap="round"
          />
          <circle cx="36" cy="32" r="2" fill="#A5F3FC" />
        </svg>
      </span>
      <span className="sp-brand-name">
        SkillPath<span>AI</span>
      </span>
    </Link>
  );
}

export default function Login() {
  const navigate = useNavigate();
  const { saveSession } = useAuth();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/api/auth/login", formData);
      saveSession(response.data);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to log in. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogleSuccess(credentialResponse) {
    if (!credentialResponse?.credential) {
      setError("Google did not return a valid sign-in credential.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const response = await api.post("/api/auth/google", {
        credential: credentialResponse.credential,
      });
      saveSession(response.data);
      navigate("/", { replace: true });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Google sign-in failed. Check the OAuth client ID and authorized app origin."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="sp-auth-screen">
      <aside className="sp-auth-showcase">
        <div className="sp-showcase-top">
          <BrandLogo />
          <span className="sp-trust-label">YOUR CAREER, YOUR PATH</span>
        </div>

        <div className="sp-showcase-content">
          <span className="sp-eyebrow">
            <span className="sp-eyebrow-dot" />
            CAREER READINESS, REIMAGINED
          </span>
          <h1>
            Your next chapter
            <br />
            starts <span>here.</span>
          </h1>
          <p>
            Build in-demand skills, discover your strengths, and make your next
            career move with confidence.
          </p>

          <div className="sp-feature-list">
            <div className="sp-feature-item">
              <span className="sp-feature-check" aria-hidden="true">
                ✓
              </span>
              Personalized career recommendations
            </div>
            <div className="sp-feature-item">
              <span className="sp-feature-check" aria-hidden="true">
                ✓
              </span>
              Clear, actionable skill pathways
            </div>
            <div className="sp-feature-item">
              <span className="sp-feature-check" aria-hidden="true">
                ✓
              </span>
              Progress you can see and celebrate
            </div>
          </div>
        </div>

        <div className="sp-showcase-footer">
          <span className="sp-footer-line" />
          <span>Learn. Practice. Build your future.</span>
        </div>
      </aside>

      <section className="sp-auth-main" aria-labelledby="login-title">
        <div className="sp-auth-mobile-brand">
          <BrandLogo />
        </div>

        <div className="sp-auth-card">
          <div className="sp-form-heading">
            <span className="sp-form-kicker">WELCOME BACK</span>
            <h2 id="login-title">Sign in to SkillPath</h2>
            <p>Pick up where you left off on your learning journey.</p>
          </div>

          {error && (
            <div className="sp-auth-error" role="alert">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="sp-auth-form">
            <div className="sp-field">
              <label htmlFor="email">Email address</label>
              <input
                id="email"
                type="email"
                name="email"
                autoComplete="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="sp-field">
              <div className="sp-label-row">
                <label htmlFor="password">Password</label>
              </div>
              <div className="sp-password-field">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  name="password"
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                <button
                  type="button"
                  className="sp-password-toggle"
                  onClick={() => setShowPassword((value) => !value)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="sp-submit-button"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
              {!loading && <span aria-hidden="true">→</span>}
            </button>
          </form>

          <div className="sp-divider">
            <span>or continue with</span>
          </div>

          <div className="sp-google-login">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() =>
                setError(
                  "Google Sign-In origin error (403): Add http://localhost:5173 and http://127.0.0.1:5173 to Authorized JavaScript origins in Google Cloud Console."
                )
              }
              shape="rectangular"
              theme="outline"
              size="large"
              text="signin_with"
              width="320"
            />
          </div>

          <p className="sp-auth-switch">
            New to SkillPath? <Link to="/register">Create an account</Link>
          </p>
        </div>

      </section>
    </main>
  );
}
