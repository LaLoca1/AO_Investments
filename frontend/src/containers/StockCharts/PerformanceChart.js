import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
  Title,
  Tooltip,
  Legend
);

const PerformanceChart = () => {
  const [timePeriod, setTimePeriod] = useState('daily');
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const endpoint = `watchlist/api/user/${timePeriod}-portfolio-performance/`;
        const response = await axios.get(endpoint);
        const data = response.data;
        setChartData({
          labels: data.map(item => item[timePeriod]),
          datasets: [
            {
              label: 'Portfolio Value',
              data: data.map(item => item.total_value),
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
  }, [timePeriod]);

  const chartOptions = {
    scales: {
      x: {
        type: 'time',
        time: {
          unit: timePeriod,
          parser: 'yyyy-MM-dd',
          displayFormats: {
            day: 'MMM dd',
            week: 'MMM dd',
            month: 'MMM yyyy'
          }
        },
        title: {
          display: true,
          text: 'Date'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Value ($)'
        }
      }
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ width: "500px", height: "400px", margin: "auto" }}>
      <h2>Portfolio Performance</h2>
      <button onClick={() => setTimePeriod('daily')}>Daily</button>
      <button onClick={() => setTimePeriod('weekly')}>Weekly</button>
      <button onClick={() => setTimePeriod('monthly')}>Monthly</button>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
};

export default PerformanceChart;
