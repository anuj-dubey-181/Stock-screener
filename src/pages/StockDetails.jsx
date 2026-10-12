import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
    ArrowLeft,
    RefreshCw,
    TrendingUp,
    Building2,
    BriefcaseBusiness,
    Bell,
    BarChart3,
    Activity
} from "lucide-react";

import { apiRequest } from '../services/api'

function StockDetails() {

    const { symbol } = useParams();
    const navigate = useNavigate();

    const [stock, setStock] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // =====================================================
    // LOAD STOCK DETAILS
    // =====================================================

    async function loadStock() {

        try {

            setLoading(true);
            setError("");

            const response =
                await apiRequest(
                    `/stocks/${encodeURIComponent(symbol)}`
                );

            const data =
                response?.data ||
                response;

            setStock(data);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to load stock details."
            );

        } finally {

            setLoading(false);

        }

    }


    useEffect(() => {

        loadStock();

    }, [symbol]);


    // =====================================================
    // FORMATTERS
    // =====================================================

    function currency(value) {

        if (
            value === null ||
            value === undefined
        ) {
            return "N/A";
        }

        return `₹${Number(value).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 2
            }
        )}`;

    }


    function number(value) {

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


    function percentage(value) {

        if (
            value === null ||
            value === undefined
        ) {
            return "N/A";
        }

        return `${Number(value).toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 2
            }
        )}%`;

    }


    // =====================================================
    // LOADING
    // =====================================================

    if (loading) {

        return (

            <div className="stock-details-loading">

                < RefreshCw
                   size={26}
                    className="stock-details-spinner"
                />

                <p>
                    Loading {symbol} details...
                </p>

            </div>

        );

    }


    // =====================================================
    // ERROR
    // =====================================================

    if (error || !stock) {

        return (

            <div className="stock-details-error-page">

                <Building2 size={40} />

                <h2>
                    Unable to load stock
                </h2>

                <p>
                    {error || "Stock details not found."}
                </p>

                <button
                    onClick={() =>
                        navigate("/stocks")
                    }
                >
                    Back to Stocks
                </button>

            </div>

        );

    }


    const company =
        stock.company || {};

    const fundamentals =
        stock.fundamentals || {};

    const historical =
        stock.historical || {};


    const currentPrice =
        historical.close_price;


    function handleBuy() {
        navigate("/portfolio", {
            state: {
                symbol: company.symbol,
                companyName: company.company_name,
                action: "buy"
            }
        })
    }

    function handleAlert() {
        navigate("/alerts", {
            state: {
                symbol: company.symbol
            }
        })
    }
    


    return (

        <div className="stock-details-page">


            {/* =================================================
                TOP BAR
            ================================================= */}

            <div className="stock-details-topbar">

                <button
                    className="back-button"
                    onClick={() =>
                        navigate("/stocks")
                    }
                >

                    <ArrowLeft size={17} />

                    Back to Stocks

                </button>


                <button
                    className="details-refresh"
                    onClick={loadStock}
                >

                    <RefreshCw size={15} />

                    Refresh

                </button>

            </div>


            {/* =================================================
                COMPANY HEADER
            ================================================= */}

            <div className="company-header-card">

                <div className="company-heading">

                    <div className="company-symbol">

                        {company.symbol}

                    </div>


                    <div>

                        <h1>
                            {company.company_name}
                        </h1>

                        <div className="company-meta">

                            <span>
                                {company.sector || "N/A"}
                            </span>

                            <span>
                                {company.industry || "N/A"}
                            </span>

                            <span>
                                {company.exchange || "N/A"}
                            </span>

                        </div>

                    </div>

                </div>


                <div className="company-price">

                    <span>
                        Current Price
                    </span>

                    <strong>
                        {currency(currentPrice)}
                    </strong>

                </div>

            </div>


            {/* =================================================
                QUICK ACTIONS
            ================================================= */}

            <div className="stock-actions">

                <button
                    className="primary-action"
                    onClick={handleBuy}
                >
                    Buy Stock
                </button>

                <button
                    className="secondary-action"
                    onClick={handleAlert}
                >
                    Create Alert
                </button>

                <button
                    className="secondary-action"
                    onClick={() => navigate("/stocks")}
                >
                    Back to Stocks
                </button>
            </div>


            {/* =================================================
                VALUATION
            ================================================= */}

            <section className="details-section">

                <div className="details-section-heading">

                    <div className="section-heading-icon purple">

                        <TrendingUp size={18} />

                    </div>

                    <div>

                        <h2>
                            Valuation
                        </h2>

                        <p>
                            Key valuation and market metrics.
                        </p>

                    </div>

                </div>


                <div className="metric-grid">


                    <Metric
                        label="Market Cap"
                        value={
                            currency(
                                fundamentals.market_cap
                            )
                        }
                    />

                    <Metric
                        label="Enterprise Value"
                        value={
                            currency(
                                fundamentals.enterprise_value
                            )
                        }
                    />

                    <Metric
                        label="P/E Ratio"
                        value={
                            number(
                                fundamentals.pe_ratio
                            )
                        }
                    />

                    <Metric
                        label="Forward P/E"
                        value={
                            number(
                                fundamentals.forward_pe
                            )
                        }
                    />

                    <Metric
                        label="PEG Ratio"
                        value={
                            number(
                                fundamentals.peg_ratio
                            )
                        }
                    />

                    <Metric
                        label="Price / Book"
                        value={
                            number(
                                fundamentals.price_to_book
                            )
                        }
                    />

                    <Metric
                        label="Dividend Yield"
                        value={
                            percentage(
                                fundamentals.dividend_yield
                            )
                        }
                    />

                    <Metric
                        label="EPS"
                        value={
                            currency(
                                fundamentals.eps
                            )
                        }
                    />

                </div>

            </section>


            {/* =================================================
                FINANCIALS
            ================================================= */}

            <section className="details-section">

                <div className="details-section-heading">

                    <div className="section-heading-icon blue">

                        <Activity size={18} />

                    </div>

                    <div>

                        <h2>
                            Financial Performance
                        </h2>

                        <p>
                            Latest reported financial metrics.
                        </p>

                    </div>

                </div>


                <div className="metric-grid">

                    <Metric
                        label="Revenue"
                        value={
                            currency(
                                fundamentals.revenue
                            )
                        }
                    />

                    <Metric
                        label="EBITDA"
                        value={
                            currency(
                                fundamentals.ebitda
                            )
                        }
                    />

                    <Metric
                        label="Net Income"
                        value={
                            currency(
                                fundamentals.net_income
                            )
                        }
                    />

                    <Metric
                        label="Total Cash"
                        value={
                            currency(
                                fundamentals.total_cash
                            )
                        }
                    />

                    <Metric
                        label="Total Debt"
                        value={
                            currency(
                                fundamentals.total_debt
                            )
                        }
                    />

                    <Metric
                        label="ROE"
                        value={
                            percentage(
                                fundamentals.roe * 100
                            )
                        }
                    />

                    <Metric
                        label="ROA"
                        value={
                            percentage(
                                fundamentals.roa * 100
                            )
                        }
                    />

                    <Metric
                        label="Report Date"
                        value={
                            fundamentals.report_date ||
                            "N/A"
                        }
                    />

                </div>

            </section>


            {/* =================================================
                MARKET DATA
            ================================================= */}

            <section className="details-section">

                <div className="details-section-heading">

                    <div className="section-heading-icon green">

                        <BarChart3 size={18} />

                    </div>

                    <div>

                        <h2>
                            Market Data
                        </h2>

                        <p>
                            Latest available trading information.
                        </p>

                    </div>

                </div>


                <div className="market-data-grid">


                    <MarketData
                        label="Open"
                        value={
                            currency(
                                historical.open_price
                            )
                        }
                    />


                    <MarketData
                        label="High"
                        value={
                            currency(
                                historical.high_price
                            )
                        }
                    />


                    <MarketData
                        label="Low"
                        value={
                            currency(
                                historical.low_price
                            )
                        }
                    />


                    <MarketData
                        label="Close"
                        value={
                            currency(
                                historical.close_price
                            )
                        }
                    />


                    <MarketData
                        label="Adjusted Close"
                        value={
                            currency(
                                historical.adjusted_close
                            )
                        }
                    />


                    <MarketData
                        label="Volume"
                        value={
                            number(
                                historical.volume
                            )
                        }
                    />

                </div>

            </section>


            {/* =================================================
                GROWTH
            ================================================= */}

            <section className="details-section">

                <div className="details-section-heading">

                    <div className="section-heading-icon orange">

                        <TrendingUp size={18} />

                    </div>

                    <div>

                        <h2>
                            Growth Indicators
                        </h2>

                        <p>
                            Available growth metrics.
                        </p>

                    </div>

                </div>


                <div className="growth-cards">


                    <div className="growth-card">

                        <span>
                            Revenue Growth
                        </span>

                        <strong>
                            {percentage(
                                historical.revenue_growth
                                    !== null &&
                                historical.revenue_growth
                                    !== undefined
                                    ? historical.revenue_growth * 100
                                    : null
                            )}
                        </strong>

                    </div>


                    <div className="growth-card">

                        <span>
                            Profit Growth
                        </span>

                        <strong>
                            {percentage(
                                historical.profit_growth
                                    !== null &&
                                historical.profit_growth
                                    !== undefined
                                    ? historical.profit_growth * 100
                                    : null
                            )}
                        </strong>

                    </div>


                </div>

            </section>


            {/* =================================================
                FOOTER NOTE
            ================================================= */}

            <div className="stock-details-note">

                <span>
                    <Activity size={14} />

                    Data shown is based on the latest
                    information available from the API.

                </span>

            </div>


        </div>

    );

}


// =====================================================
// METRIC COMPONENT
// =====================================================

function Metric({ label, value }) {

    return (

        <div className="metric-card">

            <span>
                {label}
            </span>

            <strong>
                {value}
            </strong>

        </div>

    );

}


// =====================================================
// MARKET DATA COMPONENT
// =====================================================

function MarketData({ label, value }) {

    return (

        <div className="market-data-card">

            <span>
                {label}
            </span>

            <strong>
                {value}
            </strong>

        </div>

    );

}


export default StockDetails;