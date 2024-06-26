import React from 'react'; 
import SectorBreakdownChart from '../StockCharts/SectorBreakdownChart';
import StockQuantityChart from '../StockCharts/StockQuantityChart';
import PortfolioPerformanceChart from '../StockCharts/PortfolioPerformanceChart';
import WeeklyPortfolioPerformanceChart from '../StockCharts/WeeklyPerformanceChart';
import DailyPerformanceChart from '../StockCharts/DailyPerformanceChart';
import PortfolioPeriodPerformanceChart from '../StockCharts/PortfolioPeriodPerformanceChart';
import MonthlyPortfolioPerformanceChart from '../StockCharts/MonthlyPerformanceChart';
import './Dashboard.css';

const Dashboard = () => (
    <div className='container large-gap'>
        <div className='main-content'>
            <h1 className="dashboard-title">Stock Portfolio Breakdown</h1>
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
                <div className="col-md-12"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <MonthlyPortfolioPerformanceChart/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <DailyPerformanceChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="p-8 mb-3"> {/* Increase padding for larger box */}
                        <WeeklyPortfolioPerformanceChart/>
                    </div>
                </div>
            </div>
        </div>
    </div>
); 

export default Dashboard;
