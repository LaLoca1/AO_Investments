import React from 'react'; 
import SectorBreakdownChart from '../SectorBreakdownChart';
import StockQuantityChart from '../StockQuantityChart';
import PortfolioPerformanceChart from '../PortfolioPerformanceChart';
import WeeklyPortfolioPerformanceChart from '../WeeklyPerformanceChart';
import DailyPerformanceChart from '../DailyPerformanceChart';
import PortfolioPeriodPerformanceChart from '../PortfolioPeriodPerformanceChart';
import './Dashboard.css';

const Dashboard = () => (
    <div className='container large-gap'>
        <div className='main-content'>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="border rounded p-8 mb-3 component-box"> {/* Increase padding for larger box */}
                        <SectorBreakdownChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="border rounded p-8 mb-3 component-box"> {/* Increase padding for larger box */}
                        <StockQuantityChart/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="border rounded p-8 mb-3 component-box"> {/* Increase padding for larger box */}
                        <PortfolioPerformanceChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="border rounded p-8 mb-3 component-box"> {/* Increase padding for larger box */}
                        <PortfolioPeriodPerformanceChart/>
                    </div>
                </div>
            </div>
            <div className="row">
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="border rounded p-8 mb-3 component-box"> {/* Increase padding for larger box */}
                        <WeeklyPortfolioPerformanceChart/>
                    </div>
                </div>
                <div className="col-md-6"> {/* Increase column width to make it larger */}
                    <div className="border rounded p-8 mb-3 component-box"> {/* Increase padding for larger box */}
                        <DailyPerformanceChart/>
                    </div>
                </div>
            </div>
        </div>
    </div>
); 

export default Dashboard;
