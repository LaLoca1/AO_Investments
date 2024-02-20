import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale);

const generateColors = (count) => {
  const colors = [];
  const hueStep = 360 / count; // Divide the color wheel into 'count' parts

  for (let i = 0; i < count; i++) {
    const hue = i * hueStep; // Calculate the hue value
    colors.push(`hsl(${hue}, 70%, 60%)`); // You can adjust saturation and lightness as needed
  }

  return colors;
};

const setupChartData = (data) => {
  const backgroundColors = generateColors(data.length);
  return {
    labels: data.map((item) => item.coin), // Changed to ticker
    datasets: [
      {
        label: "Crypto Quantities",
        data: data.map((item) => item.total_quantity), // Changed to total_quantity
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map((color) => color.replace("0.6", "1")),
        borderWidth: 1,
      },
    ],
  };
};

const CryptoQuantityChart = () => { // Component name changed
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("/crypto-transactions/api/user/crypto-quantity-breakdown/"); // Endpoint changed
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

  const chartOptions = {
    plugins: {
      title: {
        display: true,
        text: "Crypto Quantities",
        font: {
          size: 18,
        },
      },
      legend: {
        display: true,
        position: "bottom",
      },
    },
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2 style={{ textAlign: "center" }}>Crypto Quantities</h2>
      <div style={{ width: "400px", height: "400px", margin: "auto" }}>
        {chartData ? <Pie data={chartData} options={chartOptions} /> : <div>No data available</div>}
      </div>
    </div>
  );
};

export default CryptoQuantityChart;
