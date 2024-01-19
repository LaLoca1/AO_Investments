import React from 'react'; 
import SectorBreakdownChart from '../SectorBreakdownChart';
import StockQuantityChart from '../StockQuantityChart';
import PortfolioPerformanceChart from '../PortfolioPerformanceChart';
import WeeklyPortfolioPerformanceChart from '../WeeklyPerformanceChart';
import DailyPerformanceChart from '../DailyPerformanceChart';
import PortfolioPeriodPerformanceChart from '../PortfolioPeriodPerformanceChart';

const Dashboard = () => (
    <div className='container'>
        <div className='mt-5 p-5 bg-light'>
            <div className="row">
                <div className="col-md-6"><SectorBreakdownChart/></div>
                <div className="col-md-6"><StockQuantityChart/></div>
            </div>
            <div className="row">
                <div className="col-md-6"><PortfolioPerformanceChart/></div>
                <div className="col-md-6"><PortfolioPeriodPerformanceChart/></div>
            </div>
            <div className="row">
                <div className="col-md-6"><WeeklyPortfolioPerformanceChart/></div>
                <div className="col-md-6"><DailyPerformanceChart/></div>
            </div>
        </div>
    </div>
); 

export default Dashboard;
