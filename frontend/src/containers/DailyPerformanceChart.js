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
  TimeScale,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
  Title,
  Tooltip,
  Legend,
);

const DailyPerformanceChart = () => {
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("watchlist/api/user/daily-portfolio-performance/");
        const data = response.data;
        if (Array.isArray(data)) {
          setChartData({
            labels: data.map(item => item.day),
            datasets: [
              {
                label: 'Portfolio Value',
                data: data.map(item => item.total_value),
                percentageReturns: data.map(item => item.percentage_return),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
              }
            ]
          });
        } else {
          throw new Error("Received data is not an array");
        }
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
          text: 'Value'
        }
      }
    },
    tooltips: {
      callbacks: {
        label: function(tooltipItem, data) {
          let label = data.labels[tooltipItem.index];
          let value = data.datasets[0].data[tooltipItem.index];
          let percentageReturn = data.datasets[0].percentageReturns[tooltipItem.index];
          let returnLabel = percentageReturn != null 
                            ? `Return: ${percentageReturn.toFixed(2)}%` 
                            : 'Return: N/A';
          return `${label}: Value - ${value}, ${returnLabel}`;
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
    <div style={{ width: "600px", height: "400px", margin: "auto" }}>
      <h2 style={{ textAlign: "center" }}>Daily Portfolio Performance</h2>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
};

export default DailyPerformanceChart;
