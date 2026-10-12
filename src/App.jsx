import {
    Routes,
    Route,
    Navigate
} from "react-router-dom"

import Layout from "./components/Layout"

import Login from "./pages/Login"
import Register from "./pages/Register"
import Dashboard from "./pages/Dashboard"
import Screener from "./pages/Screener"
import Stocks from "./pages/Stocks"
import Portfolio from "./pages/Portfolio"
import Alerts from "./pages/alerts"
import StockDetails from "./pages/StockDetails"

function ProtectedRoute({ children }) {

    const token = localStorage.getItem("access_token")

    if (!token) {
        return <Navigate to="/login" replace />
    }

    return children
}


function App() {

    return (

        

            <Routes>

                {/* PUBLIC */}

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />


                {/* PROTECTED */}

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Dashboard />
                            </Layout>
                        </ProtectedRoute>
                    }
                />


                <Route
                    path="/screener"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Screener />
                            </Layout>
                        </ProtectedRoute>
                    }
                />


                <Route
                    path="/stocks"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Stocks />
                            </Layout>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/stocks/:symbol"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <StockDetails />
                            </Layout>
                        </ProtectedRoute>
                    }
                />


                <Route
                    path="/portfolio"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Portfolio />
                            </Layout>
                        </ProtectedRoute>
                    }
                />


                <Route
                    path="/alerts"
                    element={
                        <ProtectedRoute>
                            <Layout>
                                <Alerts />
                            </Layout>
                        </ProtectedRoute>
                    }
                />


                {/* DEFAULT */}

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/dashboard"
                            replace
                        />
                    }
                />


                <Route
                    path="*"
                    element={
                        <Navigate
                            to="/dashboard"
                            replace
                        />
                    }
                />

            </Routes>

       

    )
}


export default App