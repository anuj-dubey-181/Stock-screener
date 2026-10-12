
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Eye, EyeOff, TrendingUp, ShieldCheck } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import "./Auth.css";

function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(event) {
    event.preventDefault();
    setError("");

    if (!email.trim() || !password) {
      setError("Please enter your email and password.");
      return;
    }

    setLoading(true);

    try {
      await login(email.trim(), password);
      navigate("/dashboard");
    } catch (error) {
      console.error("Login error:", error);
      setError(error.message || "Login failed. Please try again.");
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
              <TrendingUp size={17} /> Smarter investing starts here
            </div>

            <p className="auth-eyebrow">WELCOME BACK</p>
            <h1>Good to see you again.</h1>
            <p className="auth-subtitle">
              Sign in to explore market opportunities and manage
              your investment watchlist.
            </p>

            <form onSubmit={handleLogin} className="auth-form">
              <div className="auth-field">
                <label htmlFor="login-email">Email address</label>
                <input
                  id="login-email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                />
              </div>

              <div className="auth-field">
                <div className="auth-label-row">
                  <label htmlFor="login-password">Password</label>
                </div>

                <div className="auth-password-wrap">
                  <input
                    id="login-password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="Enter your password"
                    autoComplete="current-password"
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
              </div>

              {error && (
                <div className="auth-message auth-error" role="alert">
                  {error}
                </div>
              )}

              <button
                type="submit"
                className="auth-submit"
                disabled={loading}
              >
                {loading ? "Signing you in..." : "Sign in to your account"}
                {!loading && <span aria-hidden="true">→</span>}
              </button>
            </form>

            <p className="auth-switch">
              New to StockPilot?
              <button type="button" onClick={() => navigate("/register")}>
                Create an account
              </button>
            </p>

            <div className="auth-security">
              <ShieldCheck size={16} />
              <span>Your account is protected by secure authentication.</span>
            </div>
          </div>
        </div>

        <aside className="auth-visual-panel">
          <div className="auth-orb auth-orb-one" />
          <div className="auth-orb auth-orb-two" />

          <div className="auth-visual-top">
            <span className="auth-live-dot" />
            YOUR MARKET INTELLIGENCE, REIMAGINED
          </div>

          <div className="auth-visual-copy">
            <p className="auth-visual-kicker">THINK BEYOND THE TICKER</p>
            <h2>Find the signal in a world of noise.</h2>
            <p>
              Screen stocks, evaluate financial metrics, and turn
              market data into clearer investment insights.
            </p>
          </div>

          <div className="auth-market-card">
            <div className="auth-market-card-head">
              <div>
                <span className="auth-market-label">YOUR ADVANTAGE</span>
                <h3>Research with purpose.</h3>
              </div>
              <span className="auth-chart-icon">
                <TrendingUp size={22} />
              </span>
            </div>

            <div className="auth-chart">
              <div className="auth-chart-grid">
                <span />
                <span />
                <span />
                <span />
              </div>
              <svg
                viewBox="0 0 420 125"
                preserveAspectRatio="none"
                role="img"
                aria-label="Decorative rising market trend"
              >
                <defs>
                  <linearGradient id="authChartFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#51e0bd" stopOpacity=".30" />
                    <stop offset="100%" stopColor="#51e0bd" stopOpacity="0" />
                  </linearGradient>
                </defs>
                <path
                  d="M0 104 L36 87 L68 94 L105 60 L137 74 L173 49 L208 62 L248 30 L280 43 L315 18 L352 35 L385 9 L420 15 L420 125 L0 125 Z"
                  fill="url(#authChartFill)"
                />
                <path
                  d="M0 104 L36 87 L68 94 L105 60 L137 74 L173 49 L208 62 L248 30 L280 43 L315 18 L352 35 L385 9 L420 15"
                  fill="none"
                  stroke="#51e0bd"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  vectorEffect="non-scaling-stroke"
                />
                <circle cx="385" cy="9" r="4" fill="#51e0bd" />
              </svg>
            </div>

            <div className="auth-market-foot">
              <span><span className="auth-live-dot" /> Data-led decisions</span>
              <span>Built for curious investors</span>
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

export default Login;