import React from 'react'; 
import CryptoPortfolioPerformanceChart from '../CryptoCharts/CryptoPortfolioPerformanceChart';
import CryptoPortfolioPeriodPerformanceChart from '../CryptoCharts/CryptoPortfolioPeriodPerformanceChart';
import CryptoWeeklyPerformanceChart from '../CryptoCharts/CryptoWeeklyPerformanceChart';
import CryptoMonthlyPerformanceChart from '../CryptoCharts/CryptoMonthlyPerformanceChart';
import './Dashboard.css';

const CryptoDashboard = () => (
    <div className='container large-gap'>
        <div className='main-content'>
            <h2 className="dashboard-title">Crypto Portfolio Breakdown</h2>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <CryptoPortfolioPerformanceChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <CryptoPortfolioPeriodPerformanceChart/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <CryptoWeeklyPerformanceChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <CryptoMonthlyPerformanceChart/>
                    </div>
                </div>
            </div>
        </div>
    </div>
); 

export default CryptoDashboard;
