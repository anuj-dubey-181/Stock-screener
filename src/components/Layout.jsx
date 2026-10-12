import { NavLink, useNavigate } from 'react-router-dom'
import {
    LayoutDashboard,
    Search,
    TrendingUp,
    Briefcase,
    Bell,
    History,
    LogOut,
    Menu,
    X
} from 'lucide-react'

import { useState } from 'react'


function Layout({ children }) {

    const navigate = useNavigate()

    const [sidebarOpen, setSidebarOpen] =
        useState(false)


    function handleLogout() {

        localStorage.removeItem('access_token')

        navigate('/login')

    }


    const navigation = [

        {
            name: 'Dashboard',
            path: '/dashboard',
            icon: LayoutDashboard
        },

        {
            name: 'AI Screener',
            path: '/screener',
            icon: Search
        },

        {
            name: 'Stocks',
            path: '/stocks',
            icon: TrendingUp
        },

        {
            name: 'Portfolio',
            path: '/portfolio',
            icon: Briefcase
        },

        {
            name: 'Alerts',
            path: '/alerts',
            icon: Bell
        },

        {
            name: 'Transactions',
            path: '/portfolio/history',
            icon: History
        }

    ]


    return (

        <div className="app-container">


            {/* ================================= */}
            {/* MOBILE HEADER */}
            {/* ================================= */}

            <header className="mobile-header">

                <button
                    onClick={() =>
                        setSidebarOpen(true)
                    }
                >
                    <Menu size={24} />
                </button>


                <div className="logo">
                    AI Stock Screener
                </div>

            </header>


            {/* ================================= */}
            {/* SIDEBAR */}
            {/* ================================= */}

            <aside
                className={`sidebar ${
                    sidebarOpen
                        ? 'sidebar-open'
                        : ''
                }`}
            >

                <div className="sidebar-header">

                    <div>

                        <h2>
                            AI Stock
                        </h2>

                        <span>
                            Screener
                        </span>

                    </div>


                    <button
                        className="close-sidebar"
                        onClick={() =>
                            setSidebarOpen(false)
                        }
                    >

                        <X size={22} />

                    </button>

                </div>


                {/* Navigation */}

                <nav className="sidebar-nav">

                    {navigation.map(
                        (item) => {

                            const Icon =
                                item.icon

                            return (

                                <NavLink
                                    key={item.path}
                                    to={item.path}
                                    onClick={() =>
                                        setSidebarOpen(false)
                                    }
                                    className={({
                                        isActive
                                    }) =>
                                        `nav-item ${
                                            isActive
                                                ? 'active'
                                                : ''
                                        }`
                                    }
                                >

                                    <Icon
                                        size={20}
                                    />

                                    <span>
                                        {item.name}
                                    </span>

                                </NavLink>

                            )

                        }
                    )}

                </nav>


                {/* Logout */}

                <div className="sidebar-footer">

                    <button
                        className="logout-button"
                        onClick={handleLogout}
                    >

                        <LogOut size={20} />

                        <span>
                            Logout
                        </span>

                    </button>

                </div>

            </aside>


            {/* ================================= */}
            {/* MAIN */}
            {/* ================================= */}

            <main className="main-content">

                {children}

            </main>


        </div>

    )

}


export default Layout