
import { apiRequest } from '../services/api'


import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import {
    Bell,
    Plus,
    Trash2,
    RefreshCw,
    CheckCircle,
    AlertTriangle,
    X,
    Activity
} from "lucide-react";

function Alerts() {
    const location = useLocation();

    const prefilledSymbol = location.state?.symbol || "";
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    const [checking, setChecking] = useState({});

    const [showCreate, setShowCreate] = useState(false);

    const [error, setError] = useState("");

    const [success, setSuccess] = useState("");


    const [form, setForm] = useState({
        symbol: "",
        metric: "pe_ratio",
        operator: "<",
        value: ""
    });


    useEffect(() => {
        if (prefilledSymbol) {
            setForm(prev => ({
                ...prev,
                symbol: prefilledSymbol
            }));

            setShowCreate(true);
        }
    }, [prefilledSymbol]);


    useEffect(() => {
        loadAlerts();
    }, []);


    // =========================================
    // LOAD ALERTS
    // =========================================

    async function loadAlerts() {

        try {

            setLoading(true);
            setError("");

            const data = await apiRequest("/alerts");

            /*
             * Handles both:
             *
             * [
             *   {...}
             * ]
             *
             * and
             *
             * {
             *   results: [...]
             * }
             */

            const result =
                Array.isArray(data)
                    ? data
                    : data.results || [];

            setAlerts(result);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to load alerts."
            );

        } finally {

            setLoading(false);

        }
    }


    useEffect(() => {

        loadAlerts();

    }, []);


    // =========================================
    // CREATE ALERT
    // =========================================

    async function createAlert(event) {

        event.preventDefault();

        if (
            !form.symbol.trim() ||
            !form.value
        ) {

            setError(
                "Please enter symbol and target value."
            );

            return;
        }


        try {

            setError("");

            await apiRequest(
                "/alerts",
                {
                    method: "POST",
                    body: JSON.stringify({
                        symbol:
                            form.symbol
                                .trim()
                                .toUpperCase(),

                        field: form.metric,

                        operator:
                            form.operator,

                        target_value:
                            Number(form.value)
                    })
                }
            );


            setSuccess(
                "Alert created successfully."
            );

            setForm({
                symbol: "",
                metric: "pe_ratio",
                operator: "<",
                value: ""
            });

            setShowCreate(false);

            await loadAlerts();

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to create alert."
            );

        }
    }


    // =========================================
    // CHECK SINGLE ALERT
    // =========================================

    async function checkAlert(alertId) {

        try {

            setChecking(prev => ({
                ...prev,
                [alertId]: true
            }));

            setError("");

            const result =
                await apiRequest(
                    `/alerts/${alertId}/check`,
                    {
                        method: "POST"
                    }
                );


            /*
             * Result:
             *
             * {
             *   alert_id: 4,
             *   symbol: "INFY",
             *   metric: "pe_ratio",
             *   operator: "<",
             *   target_value: 23,
             *   current_value: 15.43,
             *   triggered: true,
             *   message: "Alert condition triggered."
             * }
             */


            setAlerts(prev =>
                prev.map(alert => {

                    if (
                        alert.id !== alertId &&
                        alert.alert_id !== alertId
                    ) {
                        return alert;
                    }

                    return {
                        ...alert,

                        current_value:
                            result.current_value,

                        triggered:
                            result.triggered,

                        check_message:
                            result.message,

                        last_checked:
                            new Date().toISOString()
                    };

                })
            );


        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to check alert."
            );

        } finally {

            setChecking(prev => ({
                ...prev,
                [alertId]: false
            }));

        }
    }


    // =========================================
    // CHECK ALL
    // =========================================

    async function checkAllAlerts() {

        for (const alert of alerts) {

            const id =
                alert.id ??
                alert.alert_id;

            await checkAlert(id);

        }
    }


    // =========================================
    // DELETE ALERT
    // =========================================

    async function deleteAlert(alertId) {

        const confirmed =
            window.confirm(
                "Are you sure you want to delete this alert?"
            );

        if (!confirmed) return;


        try {

            setError("");

            await apiRequest(
                `/alerts/${alertId}`,
                {
                    method: "DELETE"
                }
            );


            setAlerts(prev =>
                prev.filter(alert =>
                    (alert.id ??
                        alert.alert_id) !== alertId
                )
            );


            setSuccess(
                "Alert deleted successfully."
            );

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to delete alert."
            );

        }
    }


    // =========================================
    // FORMAT METRIC
    // =========================================

    function formatMetric(metric) {

        const names = {

            pe_ratio: "P/E Ratio",

            peg_ratio: "PEG Ratio",

            price_to_book:
                "Price to Book",

            market_cap:
                "Market Cap",

            revenue:
                "Revenue",

            ebitda:
                "EBITDA",

            roe: "ROE",

            roa: "ROA"

        };

        return names[metric] || metric;
    }


    // =========================================
    // FORMAT NUMBER
    // =========================================

    function formatValue(value) {

        if (
            value === null ||
            value === undefined
        ) {

            return "N/A";

        }

        return Number(value).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 2
            }
        );
    }


    // =========================================
    // RENDER
    // =========================================

    return (

        <div className="alerts-page">


            {/* HEADER */}

            <div className="alerts-header">

                <div>

                    <div className="alerts-title">

                        <Bell size={25} />

                        <h1>
                            Stock Alerts
                        </h1>

                    </div>

                    <p>
                        Monitor your custom stock
                        conditions and check them
                        whenever you want.
                    </p>

                </div>


                <div className="alerts-header-actions">

                    <button
                        className="secondary-button"
                        onClick={checkAllAlerts}
                        disabled={
                            loading ||
                            alerts.length === 0
                        }
                    >

                        <RefreshCw size={17} />

                        Check All

                    </button>


                    <button
                        className="primary-button"
                        onClick={() => {
                            setShowCreate(true);
                            setError("");
                            setSuccess("");
                        }}
                    >

                        <Plus size={17} />

                        Create Alert

                    </button>

                </div>

            </div>


            {/* SUCCESS */}

            {success && (

                <div className="alert-message success-message">

                    <CheckCircle size={18} />

                    <span>
                        {success}
                    </span>

                    <button
                        onClick={() =>
                            setSuccess("")
                        }
                    >
                        <X size={16} />
                    </button>

                </div>

            )}


            {/* ERROR */}

            {error && (

                <div className="alert-message error-message">

                    <AlertTriangle size={18} />

                    <span>
                        {error}
                    </span>

                    <button
                        onClick={() =>
                            setError("")
                        }
                    >
                        <X size={16} />
                    </button>

                </div>

            )}


            {/* CREATE ALERT */}

            {showCreate && (

                <div className="create-alert-card">

                    <div className="create-alert-header">

                        <div>

                            <h2>
                                Create Stock Alert
                            </h2>

                            <p>
                                Set a condition to
                                monitor manually.
                            </p>

                        </div>


                        <button
                            onClick={() =>
                                setShowCreate(false)
                            }
                        >

                            <X size={20} />

                        </button>

                    </div>


                    <form
                        onSubmit={createAlert}
                        className="alert-form"
                    >

                        <div className="form-field">

                            <label>
                                Stock Symbol
                            </label>

                            <input
                                value={form.symbol}
                                onChange={e =>
                                    setForm({
                                        ...form,
                                        symbol:
                                            e.target.value
                                    })
                                }
                                placeholder="e.g. INFY"
                            />

                        </div>


                        <div className="form-field">

                            <label>
                                Metric
                            </label>

                            <select
                                value={form.metric}
                                onChange={e =>
                                    setForm({
                                        ...form,
                                        metric:
                                            e.target.value
                                    })
                                }
                            >

                                <option value="pe_ratio">
                                    P/E Ratio
                                </option>

                                <option value="peg_ratio">
                                    PEG Ratio
                                </option>

                                <option value="price_to_book">
                                    Price to Book
                                </option>

                                <option value="market_cap">
                                    Market Cap
                                </option>

                                <option value="revenue">
                                    Revenue
                                </option>

                                <option value="ebitda">
                                    EBITDA
                                </option>

                                <option value="roe">
                                    ROE
                                </option>

                                <option value="roa">
                                    ROA
                                </option>

                            </select>

                        </div>


                        <div className="form-field">

                            <label>
                                Condition
                            </label>

                            <select
                                value={form.operator}
                                onChange={e =>
                                    setForm({
                                        ...form,
                                        operator:
                                            e.target.value
                                    })
                                }
                            >

                                <option value="<">
                                    Less than
                                </option>

                                <option value="<=">
                                    Less than or equal
                                </option>

                                <option value=">">
                                    Greater than
                                </option>

                                <option value=">=">
                                    Greater than or equal
                                </option>

                                <option value="=">
                                    Equal to
                                </option>

                            </select>

                        </div>


                        <div className="form-field">

                            <label>
                                Target Value
                            </label>

                            <input
                                type="number"
                                step="any"
                                value={form.value}
                                onChange={e =>
                                    setForm({
                                        ...form,
                                        value:
                                            e.target.value
                                    })
                                }
                                placeholder="e.g. 23"
                            />

                        </div>


                        <div className="form-actions">

                            <button
                                type="button"
                                className="secondary-button"
                                onClick={() =>
                                    setShowCreate(false)
                                }
                            >
                                Cancel
                            </button>

                            <button
                                type="submit"
                                className="primary-button"
                            >

                                <Plus size={16} />

                                Create Alert

                            </button>

                        </div>

                    </form>

                </div>

            )}


            {/* ALERT LIST */}

            {loading ? (

                <div className="alerts-empty">

                    <RefreshCw
                        className="loading-icon"
                        size={25}
                    />

                    <p>
                        Loading alerts...
                    </p>

                </div>

            ) : alerts.length === 0 ? (

                <div className="alerts-empty">

                    <Bell size={40} />

                    <h3>
                        No alerts yet
                    </h3>

                    <p>
                        Create an alert to monitor
                        a stock condition.
                    </p>

                    <button
                        className="primary-button"
                        onClick={() =>
                            setShowCreate(true)
                        }
                    >

                        <Plus size={16} />

                        Create Your First Alert

                    </button>

                </div>

            ) : (

                <div className="alerts-list">

                    {alerts.map(alert => {

                        const id =
                            alert.id ??
                            alert.alert_id;

                        const triggered =
                            alert.triggered === true;

                        return (

                            <div
                                className={`alert-card ${
                                    triggered
                                        ? "alert-triggered"
                                        : ""
                                }`}
                                key={id}
                            >

                                <div className="alert-card-main">

                                    <div className="alert-symbol">

                                        <Activity
                                            size={19}
                                        />

                                        <strong>
                                            {alert.symbol}
                                        </strong>

                                    </div>


                                    <div className="alert-condition">

                                        <span>
                                            {
                                                formatMetric(
                                                    alert.metric
                                                )
                                            }
                                        </span>

                                        <strong>

                                            {alert.operator}

                                            {" "}

                                            {
                                                formatValue(
                                                    alert.value ??
                                                    alert.target_value
                                                )
                                            }

                                        </strong>

                                    </div>


                                    <div className="alert-current">

                                        <span>
                                            Current Value
                                        </span>

                                        <strong>

                                            {
                                                formatValue(
                                                    alert.current_value
                                                )
                                            }

                                        </strong>

                                    </div>


                                    <div className="alert-status">

                                        {triggered ? (

                                            <span className="status-triggered">

                                                <CheckCircle
                                                    size={15}
                                                />

                                                Triggered

                                            </span>

                                        ) : (

                                            <span className="status-not-triggered">

                                                <Activity
                                                    size={15}
                                                />

                                                Not Triggered

                                            </span>

                                        )}

                                    </div>

                                </div>


                                <div className="alert-card-actions">

                                    <button
                                        className="check-button"
                                        onClick={() =>
                                            checkAlert(id)
                                        }
                                        disabled={
                                            checking[id]
                                        }
                                    >

                                        <RefreshCw
                                            size={15}
                                            className={
                                                checking[id]
                                                    ? "loading-icon"
                                                    : ""
                                            }
                                        />

                                        {checking[id]
                                            ? "Checking..."
                                            : "Check Alert"}

                                    </button>


                                    <button
                                        className="delete-button"
                                        onClick={() =>
                                            deleteAlert(id)
                                        }
                                    >

                                        <Trash2
                                            size={16}
                                        />

                                    </button>

                                </div>

                            </div>

                        );

                    })}

                </div>

            )}

        </div>

    );

}

export default Alerts;