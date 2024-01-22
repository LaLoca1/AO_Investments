import React from 'react'; 
import SectorBreakdownChart from '../StockCharts/SectorBreakdownChart';
import StockQuantityChart from '../StockCharts/StockQuantityChart';
import PortfolioPerformanceChart from '../StockCharts/PortfolioPerformanceChart';
import WeeklyPortfolioPerformanceChart from '../StockCharts/WeeklyPerformanceChart';
import DailyPerformanceChart from '../StockCharts/DailyPerformanceChart';
import PortfolioPeriodPerformanceChart from '../StockCharts/PortfolioPeriodPerformanceChart';
import './Dashboard.css';

const Dashboard = () => (
    <div className='container large-gap'>
        <div className='main-content'>
            <h2 className="dashboard-title">Stock Portfolio Breakdown</h2>
            <div className="row row-separator">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <SectorBreakdownChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <StockQuantityChart/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <PortfolioPerformanceChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <PortfolioPeriodPerformanceChart/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <WeeklyPortfolioPerformanceChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <DailyPerformanceChart/>
                    </div>
                </div>
            </div>
        </div>
    </div>
); 

export default Dashboard;
