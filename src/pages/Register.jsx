
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Eye,
  EyeOff,
  TrendingUp,
  ShieldCheck,
  CheckCircle2
} from "lucide-react";
import { apiRequest } from "../services/api";
import "./Auth.css";

function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleRegister(event) {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (!name.trim() || !email.trim() || !password) {
      setError("Please fill in all fields.");
      return;
    }

    setLoading(true);

    try {
      await apiRequest("/auth/register", {
        method: "POST",
        body: JSON.stringify({
          name: name.trim(),
          email: email.trim(),
          password
        })
      });

      setSuccess("Account created successfully. Redirecting to login...");

      setTimeout(() => {
        navigate("/login");
      }, 1200);
    } catch (error) {
      console.error("Registration error:", error);
      setError(error.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-shell">
        <div className="auth-form-panel">
          <button
            type="button"
            className="auth-brand"
            onClick={() => navigate("/login")}
            aria-label="AI Stock Screener home"
          >
            <span className="auth-brand-icon">
              <TrendingUp size={23} />
            </span>
            <span>
              <strong>StockPilot</strong>
              <small>AI STOCK SCREENER</small>
            </span>
          </button>

          <div className="auth-form-content">
            <div className="auth-mobile-badge">
              <TrendingUp size={17} /> Start your research journey
            </div>

            <p className="auth-eyebrow">GET STARTED</p>
            <h1>Build your next investing habit.</h1>
            <p className="auth-subtitle">
              Create your account to discover stocks, screen financial
              metrics, and organize your portfolio.
            </p>

            <form onSubmit={handleRegister} className="auth-form">
              <div className="auth-field">
                <label htmlFor="register-name">Full name</label>
                <input
                  id="register-name"
                  type="text"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  placeholder="Enter your full name"
                  autoComplete="name"
                  required
                />
              </div>

              <div className="auth-field">
                <label htmlFor="register-email">Email address</label>
                <input
                  id="register-email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                />
              </div>

              <div className="auth-field">
                <label htmlFor="register-password">Create password</label>
                <div className="auth-password-wrap">
                  <input
                    id="register-password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="Choose a password"
                    autoComplete="new-password"
                    required
                  />
                  <button
                    type="button"
                    className="auth-eye-button"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff size={19} /> : <Eye size={19} />}
                  </button>
                </div>
                <p className="auth-field-hint">
                  Use a strong, unique password for your account.
                </p>
              </div>

              {error && (
                <div className="auth-message auth-error" role="alert">
                  {error}
                </div>
              )}

              {success && (
                <div className="auth-message auth-success" role="status">
                  <CheckCircle2 size={18} />
                  <span>{success}</span>
                </div>
              )}

              <button
                type="submit"
                className="auth-submit"
                disabled={loading || Boolean(success)}
              >
                {loading ? "Creating your account..." : "Create your account"}
                {!loading && <span aria-hidden="true">→</span>}
              </button>
            </form>

            <p className="auth-switch">
              Already have an account?
              <button type="button" onClick={() => navigate("/login")}>
                Sign in
              </button>
            </p>

            <div className="auth-security">
              <ShieldCheck size={16} />
              <span>Your details are handled through your account API.</span>
            </div>
          </div>
        </div>

        <aside className="auth-visual-panel">
          <div className="auth-orb auth-orb-one" />
          <div className="auth-orb auth-orb-two" />

          <div className="auth-visual-top">
            <span className="auth-live-dot" />
            YOUR NEXT CHAPTER STARTS HERE
          </div>

          <div className="auth-visual-copy">
            <p className="auth-visual-kicker">LESS GUESSWORK. MORE INSIGHT.</p>
            <h2>Make research part of your routine.</h2>
            <p>
              Bring your stock discovery, financial screening, and
              portfolio tracking together in one workspace.
            </p>
          </div>

          <div className="auth-benefits">
            <div className="auth-benefit">
              <span className="auth-benefit-icon"><CheckCircle2 size={20} /></span>
              <div>
                <strong>Discover opportunities</strong>
                <p>Explore companies and sector-based listings.</p>
              </div>
            </div>
            <div className="auth-benefit">
              <span className="auth-benefit-icon"><CheckCircle2 size={20} /></span>
              <div>
                <strong>Screen with clarity</strong>
                <p>Filter companies using financial metrics.</p>
              </div>
            </div>
            <div className="auth-benefit">
              <span className="auth-benefit-icon"><CheckCircle2 size={20} /></span>
              <div>
                <strong>Track your portfolio</strong>
                <p>Keep your holdings and alerts organized.</p>
              </div>
            </div>
          </div>

          <div className="auth-visual-footer">
            <span>ANALYZE.</span>
            <span>DISCOVER.</span>
            <span>DECIDE.</span>
          </div>
        </aside>
      </section>

      <footer className="auth-page-footer">
        StockPilot · AI-powered stock research
      </footer>
    </main>
  );
}

export default Register;