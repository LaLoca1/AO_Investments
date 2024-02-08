import React from 'react'; 
import CryptoPortfolioPerformanceChart from '../CryptoCharts/CryptoPortfolioPerformanceChart';
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
            </div>
        </div>
    </div>
); 

export default CryptoDashboard;
