import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from '../services/api'
import {
    Search,
    RefreshCw,
    Building2,
    Layers3,
    ChevronRight,
    X,
    TrendingUp
} from "lucide-react";

function Stocks() {

    const navigate = useNavigate();

    const [stocks, setStocks] = useState([]);
    const [sectors, setSectors] = useState([]);

    const [search, setSearch] = useState("");
    const [selectedSector, setSelectedSector] = useState("");

    const [loading, setLoading] = useState(true);
    const [searching, setSearching] = useState(false);
    const [error, setError] = useState("");

    // =====================================================
    // LOAD ALL STOCKS
    // =====================================================

    async function loadStocks() {

        try {

            setLoading(true);
            setError("");

            const response =
                await apiRequest("/stocks");

            const data =
                Array.isArray(response)
                    ? response
                    : response?.results ||
                      response?.data ||
                      [];

            setStocks(data);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to load stocks."
            );

        } finally {

            setLoading(false);

        }

    }


    // =====================================================
    // LOAD SECTORS
    // =====================================================

    async function loadSectors() {

        try {

            const response =
                await apiRequest("/stocks/sectors");

            const data =
                Array.isArray(response)
                    ? response
                    : response?.results ||
                      response?.data ||
                      [];

            setSectors(data);

        } catch (err) {

            console.error(
                "Sector loading error:",
                err
            );

        }

    }


    // =====================================================
    // INITIAL LOAD
    // =====================================================

    useEffect(() => {

        loadStocks();
        loadSectors();

    }, []);


    // =====================================================
    // SEARCH STOCKS
    // =====================================================

    async function handleSearch(event) {

        event?.preventDefault();

        const query =
            search.trim();

        if (!query) {

            loadStocks();

            return;

        }


        try {

            setSearching(true);
            setError("");

            const response =
                await apiRequest(
                    `/stocks/search?q=${encodeURIComponent(query)}`
                );


            const data =
                Array.isArray(response)
                    ? response
                    : response?.results ||
                      response?.data ||
                      [];


            setStocks(data);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Stock search failed."
            );

        } finally {

            setSearching(false);

        }

    }


    // =====================================================
    // SECTOR FILTER
    // =====================================================

    async function handleSectorChange(event) {

        const sector =
            event.target.value;

        setSelectedSector(sector);


        if (!sector) {

            loadStocks();

            return;

        }


        try {

            setLoading(true);
            setError("");

            const response =
                await apiRequest(
                    `/stocks/sector/${encodeURIComponent(sector)}`
                );


            const data =
                Array.isArray(response)
                    ? response
                    : response?.results ||
                      response?.data ||
                      [];


            setStocks(data);

        } catch (err) {

            console.error(err);

            setError(
                err.message ||
                "Unable to load sector stocks."
            );

        } finally {

            setLoading(false);

        }

    }


    // =====================================================
    // CLEAR FILTERS
    // =====================================================

    function clearFilters() {

        setSearch("");
        setSelectedSector("");

        loadStocks();

    }


    // =====================================================
    // STOCK DETAILS
    // =====================================================

    function openStock(symbol) {

        navigate(
            `/stocks/${encodeURIComponent(symbol)}`
        );

    }


    // =====================================================
    // FORMAT SECTORS
    // =====================================================

    const sectorList =
        sectors.map(item => {

            if (typeof item === "string") {

                return item;

            }

            return (
                item.sector ||
                item.name ||
                item.value
            );

        }).filter(Boolean);


    // =====================================================
    // LOADING
    // =====================================================

    if (loading && stocks.length === 0) {

        return (

            <div className="stocks-loading">

                <RefreshCw
                    size={25}
                    className="stocks-spinner"
                />

                <p>
                    Loading stocks...
                </p>

            </div>

        );

    }


    return (

        <div className="stocks-page">


            {/* =================================================
                HEADER
            ================================================= */}

            <div className="stocks-header">

                <div>

                    <h1>
                        Stocks
                    </h1>

                    <p>
                        Explore companies, sectors
                        and financial markets.
                    </p>

                </div>


                <button
                    className="stocks-refresh"
                    onClick={() => {
                        setSearch("");
                        setSelectedSector("");
                        loadStocks();
                    }}
                >

                    <RefreshCw size={16} />

                    Refresh

                </button>

            </div>


            {/* =================================================
                ERROR
            ================================================= */}

            {error && (

                <div className="stocks-error">

                    {error}

                </div>

            )}


            {/* =================================================
                SEARCH / FILTER BAR
            ================================================= */}

            <div className="stocks-toolbar">


                <form
                    className="stock-search"
                    onSubmit={handleSearch}
                >

                    <Search size={18} />

                    <input
                        value={search}
                        onChange={e =>
                            setSearch(
                                e.target.value
                            )
                        }
                        placeholder="Search company or symbol..."
                    />


                    {search && (

                        <button
                            type="button"
                            className="clear-search"
                            onClick={() => {
                                setSearch("");
                                loadStocks();
                            }}
                        >

                            <X size={15} />

                        </button>

                    )}


                    <button
                        type="submit"
                        className="search-button"
                        disabled={searching}
                    >

                        {searching
                            ? "Searching..."
                            : "Search"
                        }

                    </button>

                </form>


                <div className="sector-filter">

                    <Layers3 size={17} />

                    <select
                        value={selectedSector}
                        onChange={
                            handleSectorChange
                        }
                    >

                        <option value="">
                            All Sectors
                        </option>

                        {sectorList.map(
                            sector => (

                                <option
                                    key={sector}
                                    value={sector}
                                >
                                    {sector}
                                </option>

                            )
                        )}

                    </select>

                </div>


                {(search || selectedSector) && (

                    <button
                        className="clear-filters"
                        onClick={clearFilters}
                    >
                        Clear
                    </button>

                )}

            </div>


            {/* =================================================
                RESULT INFO
            ================================================= */}

            <div className="stocks-result-bar">

                <div>

                    <strong>
                        {stocks.length}
                    </strong>

                    <span>
                        {" "}
                        companies found
                    </span>

                </div>


                {selectedSector && (

                    <span className="active-filter">

                        Sector: {selectedSector}

                    </span>

                )}

                {search && (

                    <span className="active-filter">

                        Search: "{search}"

                    </span>

                )}

            </div>


            {/* =================================================
                STOCK GRID
            ================================================= */}

            {stocks.length === 0 ? (

                <div className="stocks-empty">

                    <Building2 size={38} />

                    <h3>
                        No stocks found
                    </h3>

                    <p>
                        Try another company,
                        symbol or sector.
                    </p>

                    <button
                        onClick={clearFilters}
                    >
                        View All Stocks
                    </button>

                </div>

            ) : (

                <div className="stocks-grid">

                    {stocks.map(
                        (stock, index) => (

                            <div
                                className="stock-card"
                                key={
                                    stock.id ||
                                    stock.symbol ||
                                    index
                                }
                                onClick={() =>
                                    openStock(
                                        stock.symbol
                                    )
                                }
                            >

                                <div className="stock-card-top">

                                    <div className="stock-symbol">

                                        {
                                            stock.symbol
                                        }

                                    </div>


                                    <ChevronRight
                                        size={18}
                                        className="stock-arrow"
                                    />

                                </div>


                                <div className="stock-company">

                                    <h3>
                                        {
                                            stock.company_name ||
                                            stock.name ||
                                            stock.symbol
                                        }
                                    </h3>

                                    <span>
                                        {
                                            stock.exchange ||
                                            "N/A"
                                        }
                                    </span>

                                </div>


                                <div className="stock-meta">

                                    <div>

                                        <span>
                                            Sector
                                        </span>

                                        <strong>
                                            {
                                                stock.sector ||
                                                "N/A"
                                            }
                                        </strong>

                                    </div>


                                    <div>

                                        <span>
                                            Industry
                                        </span>

                                        <strong>
                                            {
                                                stock.industry ||
                                                "N/A"
                                            }
                                        </strong>

                                    </div>

                                </div>


                                <div className="stock-card-footer">

                                    <span>
                                        View Analysis
                                    </span>

                                    <TrendingUp
                                        size={15}
                                    />

                                </div>

                            </div>

                        )
                    )}

                </div>

            )}

        </div>

    );

}

export default Stocks;