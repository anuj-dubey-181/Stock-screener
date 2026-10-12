import {
    TrendingUp,
    TrendingDown
} from 'lucide-react'


function StatCard({
    title,
    value,
    subtitle,
    type = 'default',
    icon: Icon
}) {

    const isPositive =
        type === 'positive'

    const isNegative =
        type === 'negative'


    return (

        <div className="stat-card">

            <div className="stat-card-top">

                <span className="stat-card-title">
                    {title}
                </span>

                {Icon && (
                    <div className="stat-card-icon">
                        <Icon size={20} />
                    </div>
                )}

            </div>


            <div
                className={`stat-card-value ${
                    isPositive
                        ? 'positive'
                        : isNegative
                        ? 'negative'
                        : ''
                }`}
            >
                {value}
            </div>


            {subtitle && (

                <div className="stat-card-subtitle">

                    {subtitle}

                </div>

            )}

        </div>

    )
}


export default StatCard