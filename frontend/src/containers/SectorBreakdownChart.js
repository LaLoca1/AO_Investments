import React, { useState, useEffect } from "react";
import axios from "axios";
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale
  } from 'chart.js';
  import { Pie } from 'react-chartjs-2';
  
  ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale
  );
  
const SectorBreakdownChart = () => {
  const [chartData, setChartData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/watchlist/api/user/sector-breakdown/"
        );
        console.log(response.data);
        const data = response.data;
        if (data && Array.isArray(data)) {
          setChartData({
            labels: data.map((item) => item.sector),
            datasets: [
              {
                label: "Sector Breakdown",
                data: data.map((item) => item.total_investment),
                backgroundColor: [
                  "rgba(255, 99, 132, 0.6)",
                  "rgba(54, 162, 235, 0.6)",
                  "rgba(255, 206, 86, 0.6)",
                  // ... add more colors if you have more sectors
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  // ... repeat for each sector
                ],
                borderWidth: 1,
              },
            ],
          });
        } else {
          console.error("Data is not an array:", data);
        }
      } catch (error) {
        console.error("Error fetching sector data:", error);
      }
    };

    fetchData();
  }, []);

  return chartData && Object.keys(chartData).length > 0 ? (
    <Pie data={chartData} />
  ) : (
    <div>Loading...</div>
  );
};

export default SectorBreakdownChart;
