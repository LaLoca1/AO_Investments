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

const CryptoPortfolioPeriodPerformanceChart = () => {
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("crypto-transactions/api/user/crypto-portfolio-performance-period/");
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
  
  const chartOptions = {
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'day',
          parser: 'yyyy-MM-dd',
          displayFormats: {
            day: 'MMM dd'
          }
        },
        title: {
          display: true,
          text: 'Day'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Percentage (%)'
        }
      }
    }};

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ width: "500px", height: "400px", margin: "auto" }}>
      <h2 style={{ textAlign: "center" }}>Overall Holding Period Return</h2>
      <p style={{ textAlign: "center" }}> This reflects the total percentage gain / loss over the entire period your crypto investments have been active.</p>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
};

export default CryptoPortfolioPeriodPerformanceChart;
