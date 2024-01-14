import React from 'react'; 
import SectorBreakdownChart from '../SectorBreakdownChart';

const dashboard = () => (
    <div className='container'>
        <div className='mt-5 p-5 bg-light'>
            <h1 className='display-4'>Welcome to your dashboard</h1>
            <SectorBreakdownChart/>
        </div>
    </div>
); 

export default dashboard; 