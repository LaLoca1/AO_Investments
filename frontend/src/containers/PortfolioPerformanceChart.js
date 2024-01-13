import React, { useState, useEffect } from "react";
import { Line } from 'react-chartjs-2'; 
import axios from 'axios'; 

const PortfolioPerformanceChart = () => {
    const [chartData, setChartData] = useState({}); 

    const fetchChartData = async () => {
        try {
            const response = await axios.get('/api/user/portfolio/');  // API endpoint for portfolio performance data 
            console.log(response.data);
            const data = response.data; // Prcoess this data as per your API response

            setChartData({
                labels: data.map(item => item.trade_date), // Using trade_date from data 
                datasets: [
                    {
                        label: 'Portfolio Value',
                        data: data.map(item => item.portfolioValue),
                        fill: false, 
                        backgroundColor: 'rgb(75, 192, 192)',
                        borderColor: 'rgba(75, 192, 192, 0.2)',
                    },
                ],
            });
        } catch (error) {
            console.error('Error fetching chart data:', error); 
        }
    };

    useEffect(() => {
        fetchChartData();
    }, []); 

    return (
        <div>
            <h2>Portfolio Performance</h2>
            <Line data={chartData} /> 
        </div>
    );
};

export default PortfolioPerformanceChart; 