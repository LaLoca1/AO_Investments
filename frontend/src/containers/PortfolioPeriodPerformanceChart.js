import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PortfolioPeriodPerformanceChart = () => {
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("watchlist/api/user/portfolio-performance-period/");
        const data = response.data;
        setChartData({
          labels: data.map(item => item.week),
          datasets: [
            {
              label: 'Holding Period Return (%)',
              data: data.map(item => item.holding_period_return),
              fill: false,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1
            }
          ]
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ width: "600px", height: "400px", margin: "auto" }}>
      <h2 style={{ textAlign: "center" }}>Weekly Holding Period Return</h2>
      <Line data={chartData} />
    </div>
  );
};

export default PortfolioPeriodPerformanceChart;
