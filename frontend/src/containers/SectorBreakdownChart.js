import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
} from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale
);

const generateColors = (count) => {
  // Placeholder function for color generation
  const colors = [];
  for (let i = 0; i < count; i++) {
    colors.push(`rgba(${255 - i * 20}, ${99 + i * 20}, ${132 + i * 10}, 0.6)`);
  }
  return colors;
};

const setupChartData = (data) => {
  const backgroundColors = generateColors(data.length);
  return {
    labels: data.map((item) => item.sector),
    datasets: [
      {
        label: "Sector Breakdown",
        data: data.map((item) => item.total_investment),
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map(color => color.replace('0.6', '1')),
        borderWidth: 1,
      },
    ],
  };
};

const SectorBreakdownChart = () => {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/watchlist/api/user/sector-breakdown/");
        const data = response.data;
        if (data && Array.isArray(data)) {
          setChartData(setupChartData(data));
        } else {
          throw new Error("Data is not an array or is empty");
        }
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
    <div style={{ width: '400px', height: '400px' }}>
      {chartData ? <Pie data={chartData} /> : <div>No data available</div>}
    </div>
  );
};

export default SectorBreakdownChart;
