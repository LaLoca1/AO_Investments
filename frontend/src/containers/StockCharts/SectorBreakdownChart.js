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

// Arcelement - renders slices in pie 
// Tooltip - when user hovers, provides additional ingo about data point
// Legend - Displays a box that provides labels and colours corresponding to different data sets 
// CategoryScale - Used for categorical data. In pie chart, helps label and categorize each segment of chart 
// LinearScale - Scale type used for linear data. 

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale);

// Used to generate an array of RGBA color strings. Used for styling sectors in pie chart
const generateColors = (count) => {
  const colors = [];
  const hueStep = 360 / count; // Divide the color wheel into 'count' parts

  for (let i = 0; i < count; i++) {
    const hue = i * hueStep; // Calculate the hue value
    colors.push(`hsl(${hue}, 70%, 60%)`); // You can adjust saturation and lightness as needed
  }

  return colors;
};

// Takes an array of sector data and formats it into structure required for pie chart 
// Extracts labels (sector names) and data (total investments) from input data and assigns colors to each sector 
const setupChartData = (data) => {
  const backgroundColors = generateColors(data.length);
  return {
    labels: data.map((item) => item.sector),
    datasets: [
      {
        label: "Total Investment",
        data: data.map((item) => item.total_investment),
        backgroundColor: backgroundColors,
        borderColor: backgroundColors.map((color) => color.replace("0.6", "1")),
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
        const response = await axios.get(
          "/watchlist/api/user/sector-breakdown/"
        );
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
        text: "Sector Breakdown",
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
      <h2 style={{ textAlign: "center" }}>Sector Breakdown</h2>{" "}
      <p style={{ textAlign: "center" }}>
       This pie chart provides a visual representation of your investment portfolio's sector allocation. Each slice represents the proportion of your total investment in a specific sector.
      </p>
      <div style={{ width: "400px", height: "400px", margin: "auto" }}>
        {chartData ? <Pie data={chartData} options={chartOptions} /> : <div>No data available</div>}
      </div>
    </div>
  );
};

export default SectorBreakdownChart;
