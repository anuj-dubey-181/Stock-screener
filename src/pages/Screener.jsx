import { useState } from 'react'
import {
    Search,
    Sparkles,
    RefreshCw,
    ChevronDown,
    ChevronUp,
    Database,
    Code2,
    Clock3,
    Filter,
    X
} from 'lucide-react'


import { apiRequest } from '../services/api'

function Screener() {

    const [query, setQuery] = useState('')

    const [response, setResponse] = useState(null)

    const [loading, setLoading] = useState(false)

    const [error, setError] = useState('')

    const [showTechnical, setShowTechnical] =
        useState(false)


    /*
     * =========================================
     * RUN SCREENER
     * =========================================
     */

    async function runScreener(event) {

        if (event) {
            event.preventDefault()
        }


        const cleanQuery =
            query.trim()


        if (!cleanQuery) {

            setError(
                'Please enter a screening query.'
            )

            return

        }


        try {

            setLoading(true)

            setError('')

            setResponse(null)

            setShowTechnical(false)


            const data =
                await apiRequest(
                    '/screener/nlp',
                    {
                        method: 'POST',

                        body: JSON.stringify({
                            query: cleanQuery
                        })
                    }
                )


            setResponse(data)

        } catch (error) {

            console.error(
                'Screener error:',
                error
            )


            setError(
                error.message ||
                'Unable to run screener.'
            )

        } finally {

            setLoading(false)

        }

    }


    /*
     * =========================================
     * EXAMPLE QUERIES
     * =========================================
     */

    const examples = [

        'Show companies with PE below 25',

        'Show IT companies',
        
        'show healthcare companies having eps greater than 50',
        
        'Give me financial services company with peg below 1 and price/book between 1 and 1.5',

        'Show companies with market cap above 1 lakh crore',

        'Show technology companies with PE below 30'

    ]


    function useExample(example) {

        setQuery(example)

        setError('')

    }


    /*
     * =========================================
     * CLEAR
     * =========================================
     */

    function clearResults() {

        setQuery('')

        setResponse(null)

        setError('')

        setShowTechnical(false)

    }


    /*
     * =========================================
     * FORMAT VALUES
     * =========================================
     */

    function formatNumber(value) {

        if (
            value === null ||
            value === undefined
        ) {

            return 'N/A'

        }


        return new Intl.NumberFormat(
            'en-IN',
            {
                maximumFractionDigits: 2
            }
        ).format(value)

    }


    /*
     * =========================================
     * RENDER
     * =========================================
     */

    return (

        <div className="screener-page">


            {/* ================================= */}
            {/* HEADER */}
            {/* ================================= */}

            <div className="screener-header">

                <div>

                    <div className="screener-title">

                        <Sparkles
                            size={25}
                        />

                        <h1>
                            AI Stock Screener
                        </h1>

                    </div>


                    <p>
                        Describe what you are
                        looking for in natural
                        language.
                    </p>

                </div>

            </div>


            {/* ================================= */}
            {/* QUERY CARD */}
            {/* ================================= */}

            <div className="screener-query-card">


                <div className="query-label">

                    <div>

                        <Filter
                            size={18}
                        />

                        <strong>
                            What stocks are you
                            looking for?
                        </strong>

                    </div>

                </div>


                <form
                    onSubmit={runScreener}
                >

                    <div className="query-input-wrapper">

                        <Search
                            size={20}
                        />

                        <input
                            value={query}
                            onChange={(event) =>
                                setQuery(
                                    event.target.value
                                )
                            }
                            placeholder="e.g. Show companies with PE below 25"
                            disabled={loading}
                        />


                        {query && !loading && (

                            <button
                                type="button"
                                className="query-clear"
                                onClick={() =>
                                    setQuery('')
                                }
                            >

                                <X size={17} />

                            </button>

                        )}

                    </div>


                    <button
                        type="submit"
                        className="run-screener-button"
                        disabled={
                            loading ||
                            !query.trim()
                        }
                    >

                        {loading ? (

                            <>
                                <RefreshCw
                                    size={18}
                                    className="loading-icon"
                                />

                                Analyzing...

                            </>

                        ) : (

                            <>
                                <Sparkles
                                    size={18}
                                />

                                Run Screener
                            </>

                        )}

                    </button>

                </form>


                {/* EXAMPLES */}

                <div className="example-section">

                    <span>
                        Try an example:
                    </span>


                    <div className="example-buttons">

                        {examples.map(
                            (example) => (

                                <button
                                    key={example}
                                    onClick={() =>
                                        useExample(
                                            example
                                        )
                                    }
                                >

                                    {example}

                                </button>

                            )
                        )}

                    </div>

                </div>

            </div>


            {/* ================================= */}
            {/* ERROR */}
            {/* ================================= */}

            {error && (

                <div className="screener-error">

                    <div>

                        <strong>
                            Screener failed
                        </strong>

                        <span>
                            {error}
                        </span>

                    </div>


                    <button
                        onClick={() =>
                            setError('')
                        }
                    >

                        <X size={18} />

                    </button>

                </div>

            )}


            {/* ================================= */}
            {/* LOADING */}
            {/* ================================= */}

            {loading && (

                <div className="screener-loading-card">

                    <div className="ai-loading-icon">

                        <Sparkles
                            size={26}
                        />

                    </div>


                    <h3>
                        Analyzing your query
                    </h3>


                    <p>
                        Converting your request
                        into stock filters and
                        searching the database...
                    </p>

                </div>

            )}


            {/* ================================= */}
            {/* RESULTS */}
            {/* ================================= */}

            {response && !loading && (

                <div className="screener-results">


                    {/* RESULT HEADER */}

                    <div className="results-header">

                        <div>

                            <span>
                                Screening results
                            </span>

                            <h2>

                                {response.count ??
                                    response.results?.length ??
                                    0}{' '}

                                companies found

                            </h2>

                        </div>


                        <div className="result-actions">

                            {response.cached && (

                                <span className="cached-badge">

                                    Cached result

                                </span>

                            )}


                            <button
                                onClick={() =>
                                    setShowTechnical(
                                        !showTechnical
                                    )
                                }
                            >

                                <Code2
                                    size={17}
                                />

                                Technical Details

                                {showTechnical
                                    ? <ChevronUp size={16} />
                                    : <ChevronDown size={16} />
                                }

                            </button>

                        </div>

                    </div>


                    {/* QUERY SUMMARY */}

                    <div className="query-summary">

                        <span>
                            Your query
                        </span>

                        <strong>
                            "{response.query ||
                                query}"
                        </strong>

                    </div>


                    {/* RESULT TABLE */}

                    {response.results &&
                    response.results.length > 0 ? (

                        <div className="screener-results-card">

                            <div className="results-table-wrapper">

                                <table className="screener-results-table">

                                    <thead>

                                        <tr>

                                            <th>
                                                #
                                            </th>

                                            <th>
                                                Symbol
                                            </th>

                                            <th>
                                                Company
                                            </th>

                                            <th>
                                                Sector
                                            </th>

                                            <th>
                                                Industry
                                            </th>

                                            <th>
                                                Exchange
                                            </th>

                                        </tr>

                                    </thead>


                                    <tbody>

                                        {response.results.map(
                                            (stock, index) => (

                                                <tr
                                                    key={
                                                        stock.id ||
                                                        stock.symbol ||
                                                        index
                                                    }
                                                >

                                                    <td className="result-number">

                                                        {index + 1}

                                                    </td>


                                                    <td>

                                                        <strong className="result-symbol">

                                                            {
                                                                stock.symbol
                                                            }

                                                        </strong>

                                                    </td>


                                                    <td>

                                                        {
                                                            stock.company_name
                                                        }

                                                    </td>


                                                    <td>

                                                        <span className="result-sector">

                                                            {
                                                                stock.sector
                                                            }

                                                        </span>

                                                    </td>


                                                    <td>

                                                        {
                                                            stock.industry
                                                        }

                                                    </td>


                                                    <td>

                                                        {
                                                            stock.exchange
                                                        }

                                                    </td>

                                                </tr>

                                            )
                                        )}

                                    </tbody>

                                </table>

                            </div>

                        </div>

                    ) : (

                        <div className="no-results">

                            <Filter
                                size={40}
                            />

                            <h3>
                                No matching companies
                            </h3>

                            <p>
                                Try relaxing one or
                                more of your filters.
                            </p>

                        </div>

                    )}


                    {/* ================================= */}
                    {/* EXECUTION INFORMATION */}
                    {/* ================================= */}

                    <div className="execution-summary">


                        <div className="execution-stat">

                            <Clock3
                                size={18}
                            />

                            <div>

                                <span>
                                    Execution Time
                                </span>

                                <strong>
                                    {
                                        response.execution_time !==
                                        undefined
                                            ? `${Number(
                                                response.execution_time
                                            ).toFixed(4)} sec`
                                            : 'N/A'
                                    }
                                </strong>

                            </div>

                        </div>


                        <div className="execution-stat">

                            <Database
                                size={18}
                            />

                            <div>

                                <span>
                                    Results
                                </span>

                                <strong>
                                    {
                                        response.count ??
                                        response.results?.length ??
                                        0
                                    }
                                </strong>

                            </div>

                        </div>


                        <div className="execution-stat">

                            <Sparkles
                                size={18}
                            />

                            <div>

                                <span>
                                    Source
                                </span>

                                <strong>
                                    AI Screener
                                </strong>

                            </div>

                        </div>

                    </div>


                    {/* ================================= */}
                    {/* TECHNICAL DETAILS */}
                    {/* ================================= */}

                    {showTechnical && (

                        <div className="technical-details">


                            {/* DSL */}

                            {response.dsl && (

                                <div className="technical-card">

                                    <div className="technical-card-header">

                                        <div>

                                            <Code2
                                                size={18}
                                            />

                                            <h3>
                                                Generated DSL
                                            </h3>

                                        </div>

                                    </div>


                                    <pre>

                                        {JSON.stringify(
                                            response.dsl,
                                            null,
                                            2
                                        )}

                                    </pre>

                                </div>

                            )}


                            {/* SQL */}

                            {response.sql && (

                                <div className="technical-card">

                                    <div className="technical-card-header">

                                        <div>

                                            <Database
                                                size={18}
                                            />

                                            <h3>
                                                Generated SQL
                                            </h3>

                                        </div>

                                    </div>


                                    <pre>

                                        {response.sql}

                                    </pre>

                                </div>

                            )}

                        </div>

                    )}

                </div>

            )}

        </div>

    )

}


export default Screener
