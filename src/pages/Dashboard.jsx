import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from '../services/api'
import {
    BriefcaseBusiness,
    TrendingUp,
    TrendingDown,
    Bell,
    Search,
    Filter,
    ArrowUpRight,
    ArrowDownRight,
    RefreshCw,
    BarChart3,
    Activity
} from "lucide-react";

function Dashboard() {

    const navigate = useNavigate();

    const [portfolio, setPortfolio] = useState([]);
    const [history, setHistory] = useState([]);
    const [alerts, setAlerts] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // =====================================================
    // LOAD DASHBOARD DATA
    // =====================================================

    async function loadDashboard() {

        try {

            setLoading(true);
            setError("");

            const [
                portfolioResponse,
                historyResponse,
                alertsResponse
            ] = await Promise.all([

                apiRequest("/portfolio"),

                apiRequest("/portfolio/history"),

                apiRequest("/alerts")

            ]);


            const portfolioData =
                Array.isArray(portfolioResponse)
                    ? portfolioResponse
                    : portfolioResponse?.results ||
                      portfolioResponse?.data ||
                      [];


            const historyData =
                Array.isArray(historyResponse)
                    ? historyResponse
                    : historyResponse?.results ||
                      historyResponse?.data ||
                      [];


            const alertsData =
                Array.isArray(alertsResponse)
                    ? alertsResponse
                    : alertsResponse?.results ||
                      alertsResponse?.data ||
                      [];


            setPortfolio(portfolioData);
            setHistory(historyData);
            setAlerts(alertsData);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to load dashboard."
            );

        } finally {

            setLoading(false);

        }

    }


    useEffect(() => {

        loadDashboard();

    }, []);


    // =====================================================
    // PORTFOLIO SUMMARY
    // =====================================================

    const summary = useMemo(() => {

        let invested = 0;
        let currentValue = 0;
        let profitLoss = 0;

        portfolio.forEach(stock => {

            invested += Number(
                stock.invested_amount || 0
            );

            currentValue += Number(
                stock.current_value || 0
            );

            profitLoss += Number(
                stock.profit_loss || 0
            );

        });


        const returnPercent =
            invested > 0
                ? (profitLoss / invested) * 100
                : 0;


        return {
            invested,
            currentValue,
            profitLoss,
            returnPercent
        };

    }, [portfolio]);


    // =====================================================
    // BEST / WORST PERFORMERS
    // =====================================================

    const sortedStocks = useMemo(() => {

        return [...portfolio].sort(
            (a, b) =>
                Number(b.profit_loss_percent || 0) -
                Number(a.profit_loss_percent || 0)
        );

    }, [portfolio]);


    const bestPerformer =
        sortedStocks.length > 0
            ? sortedStocks[0]
            : null;


    const worstPerformer =
        sortedStocks.length > 0
            ? sortedStocks[sortedStocks.length - 1]
            : null;


    // =====================================================
    // ALERT SUMMARY
    // =====================================================

    const triggeredAlerts = alerts.filter(
        alert =>
            alert.triggered === true ||
            alert.status === "triggered" ||
            alert.is_triggered === true
    );


    // =====================================================
    // FORMAT CURRENCY
    // =====================================================

    function currency(value) {

        return `₹${Number(
            value || 0
        ).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 2
            }
        )}`;

    }


    function number(value) {

        return Number(
            value || 0
        ).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 2
            }
        );

    }


    // =====================================================
    // TRANSACTION TYPE
    // =====================================================

    function transactionType(transaction) {

        return (
            transaction.type ||
            transaction.transaction_type ||
            transaction.action ||
            ""
        ).toUpperCase();

    }


    // =====================================================
    // LOADING
    // =====================================================

    if (loading) {

        return (

            <div className="dashboard-loading">

                <RefreshCw
                    size={25}
                    className="dashboard-spinner"
                />

                <p>
                    Loading dashboard...
                </p>

            </div>

        );

    }


    return (

        <div className="dashboard-page">


            {/* =================================================
                HEADER
            ================================================= */}

            <div className="dashboard-header">

                <div>

                    <h1>
                        Dashboard
                    </h1>

                    <p>
                        Your market and portfolio
                        overview at a glance.
                    </p>

                </div>


                <button
                    className="dashboard-refresh"
                    onClick={loadDashboard}
                >

                    <RefreshCw size={16} />

                    Refresh

                </button>

            </div>


            {/* =================================================
                ERROR
            ================================================= */}

            {error && (

                <div className="dashboard-error">

                    {error}

                </div>

            )}


            {/* =================================================
                SUMMARY CARDS
            ================================================= */}

            <div className="dashboard-summary">


                <div className="dashboard-card">

                    <div className="dashboard-card-icon purple">

                        <BriefcaseBusiness size={20} />

                    </div>

                    <div>

                        <span>
                            Portfolio Value
                        </span>

                        <strong>
                            {currency(
                                summary.currentValue
                            )}
                        </strong>

                    </div>

                </div>


                <div className="dashboard-card">

                    <div className="dashboard-card-icon blue">

                        <Activity size={20} />

                    </div>

                    <div>

                        <span>
                            Total Invested
                        </span>

                        <strong>
                            {currency(
                                summary.invested
                            )}
                        </strong>

                    </div>

                </div>


                <div className="dashboard-card">

                    <div
                        className={
                            summary.profitLoss >= 0
                                ? "dashboard-card-icon green"
                                : "dashboard-card-icon red"
                        }
                    >

                        {summary.profitLoss >= 0
                            ? <TrendingUp size={20} />
                            : <TrendingDown size={20} />
                        }

                    </div>

                    <div>

                        <span>
                            Profit / Loss
                        </span>

                        <strong
                            className={
                                summary.profitLoss >= 0
                                    ? "dashboard-profit"
                                    : "dashboard-loss"
                            }
                        >

                            {summary.profitLoss >= 0
                                ? "+"
                                : ""
                            }

                            {currency(
                                summary.profitLoss
                            )}

                        </strong>

                    </div>

                </div>


                <div className="dashboard-card">

                    <div className="dashboard-card-icon orange">

                        <BarChart3 size={20} />

                    </div>

                    <div>

                        <span>
                            Overall Return
                        </span>

                        <strong
                            className={
                                summary.returnPercent >= 0
                                    ? "dashboard-profit"
                                    : "dashboard-loss"
                            }
                        >

                            {summary.returnPercent >= 0
                                ? "+"
                                : ""
                            }

                            {number(
                                summary.returnPercent
                            )}
                            %

                        </strong>

                    </div>

                </div>

            </div>


            {/* =================================================
                QUICK ACTIONS
            ================================================= */}

            <div className="dashboard-section">

                <div className="dashboard-section-title">

                    <div>

                        <h2>
                            Quick Actions
                        </h2>

                        <p>
                            Jump directly to the tools
                            you use most.
                        </p>

                    </div>

                </div>


                <div className="dashboard-actions">


                    <button
                        onClick={() =>
                            navigate("/stocks")
                        }
                        className="quick-action"
                    >

                        <div className="quick-action-icon blue">
                            <Search size={20} />
                        </div>

                        <div>

                            <strong>
                                Analyze Stocks
                            </strong>

                            <span>
                                Search and explore
                                companies
                            </span>

                        </div>

                        <ArrowUpRight size={17} />

                    </button>


                    <button
                        onClick={() =>
                            navigate("/screener")
                        }
                        className="quick-action"
                    >

                        <div className="quick-action-icon purple">
                            <Filter size={20} />
                        </div>

                        <div>

                            <strong>
                                Run Screener
                            </strong>

                            <span>
                                Find stocks using
                                natural language
                            </span>

                        </div>

                        <ArrowUpRight size={17} />

                    </button>


                    <button
                        onClick={() =>
                            navigate("/portfolio")
                        }
                        className="quick-action"
                    >

                        <div className="quick-action-icon green">
                            <BriefcaseBusiness size={20} />
                        </div>

                        <div>

                            <strong>
                                View Portfolio
                            </strong>

                            <span>
                                Track holdings and
                                performance
                            </span>

                        </div>

                        <ArrowUpRight size={17} />

                    </button>


                    <button
                        onClick={() =>
                            navigate("/alerts")
                        }
                        className="quick-action"
                    >

                        <div className="quick-action-icon orange">
                            <Bell size={20} />
                        </div>

                        <div>

                            <strong>
                                Manage Alerts
                            </strong>

                            <span>
                                Monitor your stock
                                conditions
                            </span>

                        </div>

                        <ArrowUpRight size={17} />

                    </button>

                </div>

            </div>


            {/* =================================================
                PERFORMANCE
            ================================================= */}

            <div className="dashboard-grid">


                {/* BEST / WORST */}

                <div className="dashboard-section">

                    <div className="dashboard-section-title">

                        <div>

                            <h2>
                                Portfolio Performance
                            </h2>

                            <p>
                                Your best and worst
                                performing holdings.
                            </p>

                        </div>

                    </div>


                    {portfolio.length === 0 ? (

                        <div className="dashboard-empty">

                            <BriefcaseBusiness
                                size={30}
                            />

                            <p>
                                No holdings yet.
                            </p>

                            <button
                                onClick={() =>
                                    navigate("/portfolio")
                                }
                            >
                                Go to Portfolio
                            </button>

                        </div>

                    ) : (

                        <div className="performance-list">


                            {bestPerformer && (

                                <div className="performance-item">

                                    <div className="performance-stock">

                                        <div className="performance-symbol">
                                            {
                                                bestPerformer.symbol
                                            }
                                        </div>

                                        <div>

                                            <strong>
                                                Best Performer
                                            </strong>

                                            <span>
                                                {
                                                    bestPerformer.company_name ||
                                                    bestPerformer.symbol
                                                }
                                            </span>

                                        </div>

                                    </div>


                                    <div className="performance-value positive">

                                        +
                                        {number(
                                            bestPerformer.profit_loss_percent
                                        )}
                                        %

                                    </div>

                                </div>

                            )}


                            {worstPerformer && (

                                <div className="performance-item">

                                    <div className="performance-stock">

                                        <div className="performance-symbol">
                                            {
                                                worstPerformer.symbol
                                            }
                                        </div>

                                        <div>

                                            <strong>
                                                Needs Attention
                                            </strong>

                                            <span>
                                                {
                                                    worstPerformer.company_name ||
                                                    worstPerformer.symbol
                                                }
                                            </span>

                                        </div>

                                    </div>


                                    <div
                                        className={
                                            Number(
                                                worstPerformer.profit_loss_percent ||
                                                0
                                            ) >= 0
                                                ? "performance-value positive"
                                                : "performance-value negative"
                                        }
                                    >

                                        {
                                            Number(
                                                worstPerformer.profit_loss_percent ||
                                                0
                                            ) >= 0
                                                ? "+"
                                                : ""
                                        }

                                        {number(
                                            worstPerformer.profit_loss_percent
                                        )}
                                        %

                                    </div>

                                </div>

                            )}

                        </div>

                    )}

                </div>


                {/* ALERT OVERVIEW */}

                <div className="dashboard-section">

                    <div className="dashboard-section-title">

                        <div>

                            <h2>
                                Alerts
                            </h2>

                            <p>
                                Monitor your alert
                                conditions.
                            </p>

                        </div>


                        <button
                            className="section-link"
                            onClick={() =>
                                navigate("/alerts")
                            }
                        >
                            View All
                        </button>

                    </div>


                    <div className="alert-overview">

                        <div className="alert-stat">

                            <span>
                                Total Alerts
                            </span>

                            <strong>
                                {alerts.length}
                            </strong>

                        </div>


                        <div className="alert-stat triggered">

                            <span>
                                Triggered
                            </span>

                            <strong>
                                {triggeredAlerts.length}
                            </strong>

                        </div>

                    </div>


                    {triggeredAlerts.length > 0 ? (

                        <div className="triggered-alerts">

                            {triggeredAlerts
                                .slice(0, 3)
                                .map(
                                    (alert, index) => (

                                        <div
                                            className="mini-alert"
                                            key={
                                                alert.id ||
                                                alert.alert_id ||
                                                index
                                            }
                                        >

                                            <Bell size={15} />

                                            <div>

                                                <strong>
                                                    {
                                                        alert.symbol
                                                    }
                                                </strong>

                                                <span>
                                                    Alert triggered
                                                </span>

                                            </div>

                                        </div>

                                    )
                                )}

                        </div>

                    ) : (

                        <div className="no-alerts">

                            <Bell size={22} />

                            <span>
                                No triggered alerts
                            </span>

                        </div>

                    )}

                </div>

            </div>


            {/* =================================================
                RECENT TRANSACTIONS
            ================================================= */}

            <div className="dashboard-section">

                <div className="dashboard-section-title">

                    <div>

                        <h2>
                            Recent Transactions
                        </h2>

                        <p>
                            Your latest portfolio activity.
                        </p>

                    </div>


                    <button
                        className="section-link"
                        onClick={() =>
                            navigate("/portfolio")
                        }
                    >
                        View Portfolio
                    </button>

                </div>


                {history.length === 0 ? (

                    <div className="dashboard-empty">

                        <Activity size={30} />

                        <p>
                            No transactions yet.
                        </p>

                    </div>

                ) : (

                    <div className="recent-transactions">

                        {history
                            .slice(0, 5)
                            .map(
                                (transaction, index) => {

                                    const type =
                                        transactionType(
                                            transaction
                                        );

                                    const quantity =
                                        Number(
                                            transaction.quantity ||
                                            0
                                        );

                                    const price =
                                        Number(
                                            transaction.price ||
                                            0
                                        );


                                    return (

                                        <div
                                            className="recent-transaction"
                                            key={
                                                transaction.id ||
                                                index
                                            }
                                        >

                                            <div
                                                className={
                                                    type === "BUY"
                                                        ? "transaction-icon buy"
                                                        : "transaction-icon sell"
                                                }
                                            >

                                                {type === "BUY"
                                                    ? <ArrowDownRight size={17} />
                                                    : <ArrowUpRight size={17} />
                                                }

                                            </div>


                                            <div className="transaction-info">

                                                <strong>
                                                    {
                                                        transaction.symbol
                                                    }
                                                </strong>

                                                <span>

                                                    {type || "TRANSACTION"}

                                                    {" • "}

                                                    {quantity}
                                                    {" shares"}

                                                </span>

                                            </div>


                                            <div className="transaction-price">

                                                {currency(
                                                    quantity * price
                                                )}

                                            </div>

                                        </div>

                                    );

                                }
                            )}

                    </div>

                )}

            </div>


        </div>

    );

}

export default Dashboard;