import React from 'react'; 
import SectorBreakdownChart from '../SectorBreakdownChart';
import StockQuantityChart from '../StockQuantityChart';
import PortfolioPerformanceChart from '../PortfolioPerformanceChart';
import WeeklyPortfolioPerformanceChart from '../WeeklyPerformanceChart';
import DailyPerformanceChart from '../DailyPerformanceChart';

const dashboard = () => (
    <div className='container'>
        <div className='mt-5 p-5 bg-light'>
            <SectorBreakdownChart/>
            <StockQuantityChart/> 
            <PortfolioPerformanceChart/>
            <WeeklyPortfolioPerformanceChart/>
            <DailyPerformanceChart/>
        </div>
    </div>
); 

export default dashboard; 