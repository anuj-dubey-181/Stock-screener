
import { apiRequest } from '../services/api'
import Plot from "react-plotly.js";
import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import {
    BriefcaseBusiness,
    TrendingUp,
    TrendingDown,
    Plus,
    Minus,
    RefreshCw,
    History,
    X
} from "lucide-react";

function Portfolio() {

    const [holdings, setHoldings] = useState([]);
    const [history, setHistory] = useState([]);

    const [loading, setLoading] = useState(true);
    const [historyLoading, setHistoryLoading] = useState(false);

    const [showBuy, setShowBuy] = useState(false);
    const [showSell, setShowSell] = useState(false);

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const location = useLocation();

    const prefilledSymbol = location.state?.symbol || "";
    const prefilledAction = location.state?.action || "";

    const [buyForm, setBuyForm] = useState({
        symbol: "",
        quantity: "",
        price: ""
    });

    const [sellForm, setSellForm] = useState({
        symbol: "",
        quantity: "",
        price: ""
    });

    useEffect(() => {
        if (prefilledSymbol && prefilledAction === "buy") {
            setBuyForm(prev => ({
                ...prev,
                symbol: prefilledSymbol
            }));

            setShowBuy(true);
            setShowSell(false);
        }
    }, [prefilledSymbol, prefilledAction]);


    useEffect(() => {
        loadPortfolio();
        loadHistory();
    }, []);





    // =====================================================
    // LOAD PORTFOLIO
    // =====================================================

    async function loadPortfolio() {

        try {

            setLoading(true);
            setError("");

            const data =
                await apiRequest("/portfolio");

            const result =
                Array.isArray(data)
                    ? data
                    : data.results || data.data || [];

            setHoldings(result);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to load portfolio."
            );

        } finally {

            setLoading(false);

        }
    }


    // =====================================================
    // LOAD HISTORY
    // =====================================================

    async function loadHistory() {

        try {

            setHistoryLoading(true);

            const data =
                await apiRequest("/portfolio/history");

            const result =
                Array.isArray(data)
                    ? data
                    : data.results || data.data || [];

            setHistory(result);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to load transaction history."
            );

        } finally {

            setHistoryLoading(false);

        }
    }


    useEffect(() => {

        loadPortfolio();
        loadHistory();

    }, []);


    // =====================================================
    // BUY
    // =====================================================

    async function handleBuy(event) {

        event.preventDefault();

        if (
            !buyForm.symbol.trim() ||
            !buyForm.quantity ||
            !buyForm.price
        ) {

            setError(
                "Please enter symbol, quantity and price."
            );

            return;
        }


        try {

            setError("");

            await apiRequest(
                "/portfolio/buy",
                {
                    method: "POST",

                    body: JSON.stringify({

                        symbol:
                            buyForm.symbol
                                .trim()
                                .toUpperCase(),

                        quantity:
                            Number(buyForm.quantity),

                        price:
                            Number(buyForm.price)

                    })
                }
            );


            setSuccess(
                `${buyForm.symbol.toUpperCase()} added to portfolio.`
            );


            setBuyForm({
                symbol: "",
                quantity: "",
                price: ""
            });


            setShowBuy(false);

            await loadPortfolio();
            await loadHistory();

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to complete purchase."
            );

        }
    }


    // =====================================================
    // SELL
    // =====================================================

    async function handleSell(event) {

        event.preventDefault();

        if (
            !sellForm.symbol.trim() ||
            !sellForm.quantity ||
            !sellForm.price
        ) {

            setError(
                "Please enter symbol, quantity and price."
            );

            return;
        }


        try {

            setError("");

            await apiRequest(
                "/portfolio/sell",
                {
                    method: "POST",

                    body: JSON.stringify({

                        symbol:
                            sellForm.symbol
                                .trim()
                                .toUpperCase(),

                        quantity:
                            Number(sellForm.quantity),

                        price:
                            Number(sellForm.price)

                    })
                }
            );


            setSuccess(
                `${sellForm.symbol.toUpperCase()} sold successfully.`
            );


            setSellForm({
                symbol: "",
                quantity: "",
                price: ""
            });


            setShowSell(false);

            await loadPortfolio();
            await loadHistory();

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to complete sale."
            );

        }
    }


    // =====================================================
    // PORTFOLIO CALCULATIONS
    // =====================================================

    const summary = useMemo(() => {

        let invested = 0;
        let current = 0;
        let profitLoss = 0;

        holdings.forEach(stock => {

            invested +=
                Number(
                    stock.invested_amount || 0
                );

            current +=
                Number(
                    stock.current_value || 0
                );

            profitLoss +=
                Number(
                    stock.profit_loss || 0
                );

        });


        const profitLossPercent =
            invested > 0
                ? (profitLoss / invested) * 100
                : 0;


        return {
            invested,
            current,
            profitLoss,
            profitLossPercent
        };

    }, [holdings]);

    const allocationData = useMemo(() => {

    return holdings
        .filter(
            stock =>
                Number(stock.current_value || 0) > 0
        )
        .map(stock => ({
            label: stock.symbol,
            value: Number(
                stock.current_value || 0
            )
        }));

     }, [holdings]);


    const profitLossData = useMemo(() => {

    return holdings.map(stock => ({
        symbol: stock.symbol,
        profitLoss: Number(
            stock.profit_loss || 0
        )
    }));

    }, [holdings]);

    // =====================================================
    // FORMAT CURRENCY
    // =====================================================

    function currency(value) {

        return `₹${Number(value || 0).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 2
            }
        )}`;

    }


    // =====================================================
    // FORMAT NUMBER
    // =====================================================

    function number(value) {

        return Number(value || 0).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 2
            }
        );

    }


    // =====================================================
    // CLOSE MESSAGES
    // =====================================================

    function clearMessages() {

        setError("");
        setSuccess("");

    }


    return (

        <div className="portfolio-page">


            {/* =================================================
                HEADER
            ================================================= */}

            <div className="portfolio-header">

                <div>

                    <div className="portfolio-title">

                        <BriefcaseBusiness size={25} />

                        <h1>
                            My Portfolio
                        </h1>

                    </div>

                    <p>
                        Track your holdings,
                        investments and returns.
                    </p>

                </div>


                <div className="portfolio-actions">

                    <button
                        className="secondary-button"
                        onClick={() => {
                            loadPortfolio();
                            loadHistory();
                        }}
                    >

                        <RefreshCw size={16} />

                        Refresh

                    </button>


                    <button
                        className="buy-button"
                        onClick={() => {
                            clearMessages();
                            setShowBuy(true);
                            setShowSell(false);
                        }}
                    >

                        <Plus size={17} />

                        Buy

                    </button>


                    <button
                        className="sell-button"
                        onClick={() => {
                            clearMessages();
                            setShowSell(true);
                            setShowBuy(false);
                        }}
                    >

                        <Minus size={17} />

                        Sell

                    </button>

                </div>

            </div>


            {/* =================================================
                MESSAGES
            ================================================= */}

            {success && (

                <div className="portfolio-message success">

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


            {error && (

                <div className="portfolio-message error">

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


            {/* =================================================
                BUY / SELL FORM
            ================================================= */}

            {(showBuy || showSell) && (

                <div className="transaction-card">

                    <div className="transaction-header">

                        <div>

                            <h2>
                                {showBuy
                                    ? "Buy Stocks"
                                    : "Sell Stocks"}
                            </h2>

                            <p>
                                {showBuy
                                    ? "Add shares to your portfolio."
                                    : "Sell shares from your portfolio."}
                            </p>

                        </div>


                        <button
                            onClick={() => {
                                setShowBuy(false);
                                setShowSell(false);
                            }}
                        >

                            <X size={20} />

                        </button>

                    </div>


                    {showBuy && (

                        <form
                            className="transaction-form"
                            onSubmit={handleBuy}
                        >

                            <div className="form-field">

                                <label>
                                    Stock Symbol
                                </label>

                                <input
                                    value={buyForm.symbol}
                                    onChange={e =>
                                        setBuyForm({
                                            ...buyForm,
                                            symbol:
                                                e.target.value
                                        })
                                    }
                                    placeholder="e.g. TCS"
                                />

                            </div>


                            <div className="form-field">

                                <label>
                                    Quantity
                                </label>

                                <input
                                    type="number"
                                    min="1"
                                    value={buyForm.quantity}
                                    onChange={e =>
                                        setBuyForm({
                                            ...buyForm,
                                            quantity:
                                                e.target.value
                                        })
                                    }
                                    placeholder="10"
                                />

                            </div>


                            <div className="form-field">

                                <label>
                                    Buy Price
                                </label>

                                <input
                                    type="number"
                                    step="any"
                                    min="0"
                                    value={buyForm.price}
                                    onChange={e =>
                                        setBuyForm({
                                            ...buyForm,
                                            price:
                                                e.target.value
                                        })
                                    }
                                    placeholder="2450"
                                />

                            </div>


                            <div className="transaction-submit">

                                <button
                                    type="submit"
                                    className="buy-button"
                                >

                                    <Plus size={16} />

                                    Buy Stocks

                                </button>

                            </div>

                        </form>

                    )}


                    {showSell && (

                        <form
                            className="transaction-form"
                            onSubmit={handleSell}
                        >

                            <div className="form-field">

                                <label>
                                    Stock Symbol
                                </label>

                                <input
                                    value={sellForm.symbol}
                                    onChange={e =>
                                        setSellForm({
                                            ...sellForm,
                                            symbol:
                                                e.target.value
                                        })
                                    }
                                    placeholder="e.g. TCS"
                                />

                            </div>


                            <div className="form-field">

                                <label>
                                    Quantity
                                </label>

                                <input
                                    type="number"
                                    min="1"
                                    value={sellForm.quantity}
                                    onChange={e =>
                                        setSellForm({
                                            ...sellForm,
                                            quantity:
                                                e.target.value
                                        })
                                    }
                                    placeholder="5"
                                />

                            </div>


                            <div className="form-field">

                                <label>
                                    Sell Price
                                </label>

                                <input
                                    type="number"
                                    step="any"
                                    min="0"
                                    value={sellForm.price}
                                    onChange={e =>
                                        setSellForm({
                                            ...sellForm,
                                            price:
                                                e.target.value
                                        })
                                    }
                                    placeholder="2500"
                                />

                            </div>


                            <div className="transaction-submit">

                                <button
                                    type="submit"
                                    className="sell-button"
                                >

                                    <Minus size={16} />

                                    Sell Stocks

                                </button>

                            </div>

                        </form>

                    )}

                </div>

            )}


            {/* =================================================
                SUMMARY CARDS
            ================================================= */}

            <div className="portfolio-summary">

                <div className="summary-card">

                    <div className="summary-icon">
                        <BriefcaseBusiness size={19} />
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


                <div className="summary-card">

                    <div className="summary-icon">
                        <TrendingUp size={19} />
                    </div>

                    <div>

                        <span>
                            Current Value
                        </span>

                        <strong>
                            {currency(
                                summary.current
                            )}
                        </strong>

                    </div>

                </div>


                <div className="summary-card">

                    <div
                        className={
                            summary.profitLoss >= 0
                                ? "summary-icon profit"
                                : "summary-icon loss"
                        }
                    >

                        {summary.profitLoss >= 0
                            ? <TrendingUp size={19} />
                            : <TrendingDown size={19} />
                        }

                    </div>

                    <div>

                        <span>
                            Profit / Loss
                        </span>

                        <strong
                            className={
                                summary.profitLoss >= 0
                                    ? "profit-text"
                                    : "loss-text"
                            }
                        >
                            {currency(
                                summary.profitLoss
                            )}
                        </strong>

                    </div>

                </div>


                <div className="summary-card">

                    <div className="summary-icon">
                        <TrendingUp size={19} />
                    </div>

                    <div>

                        <span>
                            Overall Return
                        </span>

                        <strong
                            className={
                                summary.profitLossPercent >= 0
                                    ? "profit-text"
                                    : "loss-text"
                            }
                        >

                            {summary.profitLossPercent >= 0
                                ? "+"
                                : ""
                            }

                            {number(
                                summary.profitLossPercent
                            )}
                            %

                        </strong>

                    </div>

                </div>

            </div>



            {/* =================================================
           PORTFOLIO ANALYTICS
          ================================================= */}

        {holdings.length > 0 && (

            <div className="portfolio-analytics">

                {/* Allocation */}

                <div className="analytics-card">

                    <div className="analytics-header">

                        <div>

                            <h2>
                                Portfolio Allocation
                            </h2>

                            <span>
                                Distribution by current value
                            </span>

                        </div>

                    </div>


                    <Plot

                        data={[
                            {
                                labels:
                                    allocationData.map(
                                        item => item.label
                                    ),

                                values:
                                    allocationData.map(
                                        item => item.value
                                    ),

                                type: "pie",

                                hole: 0.55,

                                textinfo: "label+percent",

                                hovertemplate:
                                    "<b>%{label}</b><br>" +
                                    "Value: ₹%{value:,.2f}" +
                                    "<br>" +
                                    "Share: %{percent}" +
                                    "<extra></extra>"
                            }
                        ]}


                        layout={{

                            autosize: true,

                            height: 360,

                            margin: {
                                l: 20,
                        r: 20,
                        t: 20,
                        b: 20
                    },

                    showlegend: true,

                    legend: {
                        orientation: "h",
                        y: -0.05
                    },

                    paper_bgcolor:
                        "rgba(0,0,0,0)",

                    plot_bgcolor:
                        "rgba(0,0,0,0)"

                }}


                config={{
                    responsive: true,
                    displayModeBar: false
                }}


                style={{
                    width: "100%"
                }}

            />

        </div>


        {/* Profit / Loss */}

        <div className="analytics-card">

            <div className="analytics-header">

                <div>

                    <h2>
                        Profit / Loss
                    </h2>

                    <span>
                        Performance by holding
                    </span>

                </div>

            </div>


            <Plot

                data={[
                    {
                        x:
                            profitLossData.map(
                                item => item.symbol
                            ),

                        y:
                            profitLossData.map(
                                item => item.profitLoss
                            ),

                        type: "bar",

                        hovertemplate:
                            "<b>%{x}</b><br>" +
                            "P/L: ₹%{y:,.2f}" +
                            "<extra></extra>"
                    }
                ]}


                layout={{

                    autosize: true,

                    height: 360,

                    margin: {
                        l: 60,
                        r: 20,
                        t: 20,
                        b: 50
                    },

                    xaxis: {
                        title: "Stock"
                    },

                    yaxis: {
                        title: "Profit / Loss (₹)"
                    },

                    paper_bgcolor:
                        "rgba(0,0,0,0)",

                    plot_bgcolor:
                        "rgba(0,0,0,0)",

                    hovermode: "x unified"

                }}


                config={{
                    responsive: true,
                    displayModeBar: false
                }}


                style={{
                    width: "100%"
                }}

            />

               </div>

               </div>

            )}


            





            {/* =================================================
                HOLDINGS
            ================================================= */}

            <div className="portfolio-section">

                <div className="section-header">

                    <div>

                        <h2>
                            Holdings
                        </h2>

                        <span>
                            {holdings.length} stocks
                        </span>

                    </div>

                </div>


                {loading ? (

                    <div className="portfolio-empty">

                        <RefreshCw
                            className="loading-icon"
                            size={24}
                        />

                        <p>
                            Loading portfolio...
                        </p>

                    </div>

                ) : holdings.length === 0 ? (

                    <div className="portfolio-empty">

                        <BriefcaseBusiness
                            size={40}
                        />

                        <h3>
                            Your portfolio is empty
                        </h3>

                        <p>
                            Buy your first stock
                            to start tracking
                            your portfolio.
                        </p>

                    </div>

                ) : (

                    <div className="portfolio-table-wrapper">

                        <table className="portfolio-table">

                            <thead>

                                <tr>

                                    <th>
                                        Stock
                                    </th>

                                    <th>
                                        Quantity
                                    </th>

                                    <th>
                                        Avg. Buy
                                    </th>

                                    <th>
                                        Current Price
                                    </th>

                                    <th>
                                        Invested
                                    </th>

                                    <th>
                                        Current Value
                                    </th>

                                    <th>
                                        P/L
                                    </th>

                                    <th>
                                        P/L %
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {holdings.map(
                                    (stock, index) => {

                                        const profit =
                                            Number(
                                                stock.profit_loss ||
                                                0
                                            );

                                        const percent =
                                            Number(
                                                stock.profit_loss_percent ||
                                                0
                                            );


                                        return (

                                            <tr
                                                key={
                                                    stock.symbol ||
                                                    index
                                                }
                                            >

                                                <td>

                                                    <div className="stock-name">

                                                        <strong>
                                                            {
                                                                stock.symbol
                                                            }
                                                        </strong>

                                                        <span>
                                                            {
                                                                stock.company_name ||
                                                                ""
                                                            }
                                                        </span>

                                                    </div>

                                                </td>


                                                <td>
                                                    {
                                                        number(
                                                            stock.quantity
                                                        )
                                                    }
                                                </td>


                                                <td>
                                                    {
                                                        currency(
                                                            stock.avg_buy_price
                                                        )
                                                    }
                                                </td>


                                                <td>
                                                    {
                                                        currency(
                                                            stock.current_price
                                                        )
                                                    }
                                                </td>


                                                <td>
                                                    {
                                                        currency(
                                                            stock.invested_amount
                                                        )
                                                    }
                                                </td>


                                                <td>
                                                    {
                                                        currency(
                                                            stock.current_value
                                                        )
                                                    }
                                                </td>


                                                <td>

                                                    <span
                                                        className={
                                                            profit >= 0
                                                                ? "profit-text"
                                                                : "loss-text"
                                                        }
                                                    >

                                                        {profit >= 0
                                                            ? "+"
                                                            : ""
                                                        }

                                                        {
                                                            currency(
                                                                profit
                                                            )
                                                        }

                                                    </span>

                                                </td>


                                                <td>

                                                    <span
                                                        className={
                                                            percent >= 0
                                                                ? "profit-badge"
                                                                : "loss-badge"
                                                        }
                                                    >

                                                        {percent >= 0
                                                            ? "+"
                                                            : ""
                                                        }

                                                        {
                                                            number(
                                                                percent
                                                            )
                                                        }
                                                        %

                                                    </span>

                                                </td>

                                            </tr>

                                        );

                                    }
                                )}

                            </tbody>

                        </table>

                    </div>

                )}

            </div>


            {/* =================================================
                HISTORY
            ================================================= */}

            <div className="portfolio-section">

                <div className="section-header">

                    <div className="history-title">

                        <History size={20} />

                        <div>

                            <h2>
                                Transaction History
                            </h2>

                            <span>
                                Your recent portfolio activity
                            </span>

                        </div>

                    </div>

                </div>


                {historyLoading ? (

                    <div className="portfolio-empty">

                        <RefreshCw
                            className="loading-icon"
                            size={24}
                        />

                        <p>
                            Loading history...
                        </p>

                    </div>

                ) : history.length === 0 ? (

                    <div className="portfolio-empty">

                        <History size={35} />

                        <p>
                            No transactions yet.
                        </p>

                    </div>

                ) : (

                    <div className="history-table-wrapper">

                        <table className="portfolio-table">

                            <thead>

                                <tr>

                                    <th>
                                        Type
                                    </th>

                                    <th>
                                        Stock
                                    </th>

                                    <th>
                                        Quantity
                                    </th>

                                    <th>
                                        Price
                                    </th>

                                    <th>
                                        Total
                                    </th>

                                    <th>
                                        Date
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                {history.map(
                                    (transaction, index) => {

                                        const type =
                                            (
                                                transaction.type ||
                                                transaction.transaction_type ||
                                                transaction.action ||
                                                ""
                                            ).toUpperCase();


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


                                        const total =
                                            transaction.total ||
                                            quantity * price;


                                        return (

                                            <tr
                                                key={
                                                    transaction.id ||
                                                    index
                                                }
                                            >

                                                <td>

                                                    <span
                                                        className={
                                                            type === "BUY"
                                                                ? "transaction-buy"
                                                                : "transaction-sell"
                                                        }
                                                    >

                                                        {type === "BUY"
                                                            ? "+"
                                                            : "-"
                                                        }

                                                        {type || "TRANSACTION"}

                                                    </span>

                                                </td>


                                                <td>

                                                    <strong>
                                                        {
                                                            transaction.symbol
                                                        }
                                                    </strong>

                                                </td>


                                                <td>
                                                    {number(quantity)}
                                                </td>


                                                <td>
                                                    {currency(price)}
                                                </td>


                                                <td>
                                                    {currency(total)}
                                                </td>


                                                <td>

                                                    {
                                                        transaction.created_at
                                                            ? new Date(
                                                                transaction.created_at
                                                            ).toLocaleString(
                                                                "en-IN"
                                                            )
                                                            : "—"
                                                    }

                                                </td>

                                            </tr>

                                        );

                                    }
                                )}

                            </tbody>

                        </table>

                    </div>

                )}

            </div>

        </div>

    );

}

export default Portfolio;