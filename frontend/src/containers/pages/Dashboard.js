import React from 'react'; 
import SectorBreakdownChart from '../SectorBreakdownChart';
import StockQuantityChart from '../StockQuantityChart';

const dashboard = () => (
    <div className='container'>
        <div className='mt-5 p-5 bg-light'>
            <SectorBreakdownChart/>
            <StockQuantityChart/> 
        </div>
    </div>
); 

export default dashboard; 