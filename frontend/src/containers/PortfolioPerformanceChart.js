import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

const PortfolioPerformanceChart = () => {
    const [chartData, setChartData] = useState({});

    const fetchChartData = async () => {
        try {
            const response = await axios.get('/watchlist/api/user/portfolio-performance/'); // Update with your actual API endpoint
            const data = response.data;

            setChartData({
                labels: data.map(item => item.week),
                datasets: [
                    {
                        label: 'Portfolio Value',
                        data: data.map(item => item.totalValue),
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1, // Adds some curve to the line
                    },
                ],
            });
        } catch (error) {
            console.error("Error fetching chart data:", error);
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
